from hardware import button_horn
import time
import os
import random
import subprocess
from states.shared import SharedState
import yaml

# ── Config ────────────────────────────────────────────────────────────────────
base_dir  = "/home/pi/echoes-of-tomorrow/src"
audio_dir = "/home/pi/echoes-of-tomorrow/audio_files"

with open(os.path.join(base_dir, "config.yaml"), "r") as f:
    config = yaml.safe_load(f)

AUDIO_CARD = config.get("audio_card_ring", "plughw:0,0")
ring_path  = os.path.join(audio_dir, "ring.wav")
debounce = 0.3

# Switch to True to enable the random ring sound and False to disable it
ring_on = True

# Ring settings
rings_per_call = 3  # Number of rings per call
ring_interval  = 2  # Seconds between rings within a single call
calls_per_hour = 2  # How many calls to schedule per hour

# ── Hour-scheduling state (module-level, persists between run() calls) ────────
_hour_start   = None   # time.time() when the current hour window began
_call_offsets = []     # sorted list of seconds-into-hour when calls fire
_calls_fired  = set()  # indices into _call_offsets already triggered
# ─────────────────────────────────────────────────────────────────────────────


def _schedule_new_hour():
    """Pick two random moments within the next 3600-second window."""
    global _hour_start, _call_offsets, _calls_fired
    _hour_start   = time.time()
    _call_offsets = sorted(random.uniform(0, 3600) for _ in range(calls_per_hour))
    _calls_fired  = set()
    print(f"[idle] 🕐 New hour scheduled — calls at offsets: "
          f"{[f'{t:.1f}s' for t in _call_offsets]}")


def _check_horn():
    """
    Non-blocking horn check.
    Waits for release if currently pressed, then returns 'play_welcome'.
    Returns None if the horn is not being lifted.
    """
    if button_horn.is_pressed:
        while button_horn.is_pressed:   # wait for release
            time.sleep(0.01)
        print("\n📞   The horn has been picked up")
        time.sleep(debounce)
        return "play_welcome"
    return None


def _interruptible_sleep(seconds):
    """
    Sleep for `seconds` in small chunks, checking the horn each tick.
    Returns 'play_welcome' immediately if the horn is picked up, else None.
    """
    deadline = time.time() + seconds
    while time.time() < deadline:
        result = _check_horn()
        if result:
            return result
        time.sleep(0.05)
    return None


def _play_call():
    """
    Execute one full call: rings_per_call rings separated by ring_interval seconds.
    The horn is checked continuously — during playback AND during the gap between rings.
    Returns 'play_welcome' if the horn is lifted at any point, else None.
    """
    print("[idle] 📳 Incoming call — ringing…")

    for ring_num in range(rings_per_call):
        # Start the ring audio in a subprocess so we stay responsive
        try:
            proc = subprocess.Popen(
                ["aplay", "-D", AUDIO_CARD, ring_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception as e:
            print(f"[idle] Error playing ring: {e}")
            proc = None

        # Poll until the .wav finishes, checking the horn the whole time
        if proc:
            while proc.poll() is None:
                result = _check_horn()
                if result:
                    proc.terminate()
                    proc.wait()
                    return result
                time.sleep(0.05)

        # Inter-ring gap — skip after the final ring
        if ring_num < rings_per_call - 1:
            result = _interruptible_sleep(ring_interval)
            if result:
                return result

    print("[idle] 📵 Call ended (no answer)")
    return None


# ── Main state entry point ────────────────────────────────────────────────────
def run():
    global _hour_start

    # First-ever call: set up the hour schedule
    if _hour_start is None:
        _schedule_new_hour()

    # Roll over to a fresh hour window when the current one expires
    if time.time() - _hour_start >= 3600:
        _schedule_new_hour()

    # ── Always check the horn first ──
    result = _check_horn()
    if result:
        return result

    # ── Check whether a scheduled call is due ──
    if ring_on:
        elapsed = time.time() - _hour_start
        for i, offset in enumerate(_call_offsets):
            if i not in _calls_fired and elapsed >= offset:
                _calls_fired.add(i)          # mark before playing to avoid re-trigger
                result = _play_call()
                if result:
                    return result

    return None   # stay in idle