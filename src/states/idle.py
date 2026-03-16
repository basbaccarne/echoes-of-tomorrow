import time
import datetime
import os
import random
import subprocess

from hardware import button_horn
from states.shared import SharedState
from states.shared import AUDIO_CARD_RING

# ── Config ────────────────────────────────────────────────────────────────────
audio_dir = "/home/pi/echoes-of-tomorrow/audio_files"
ring_path = os.path.join(audio_dir, "ring.wav")
debounce = 0.3

# Switch to True to enable the random ring sound and False to disable it
ring_on = True

# Ring settings
rings_per_call = 3  # Number of rings per call
ring_interval  = 2  # Seconds between rings within a single call
calls_per_hour = 2  # How many calls to schedule per hour

# ── Hour-scheduling state (module-level, persists between run() calls) ────────
_hour_start   = None
_call_offsets = []
_calls_fired  = set()
# ─────────────────────────────────────────────────────────────────────────────


def _schedule_new_hour():
    """Pick random moments within the next 3600-second window."""
    global _hour_start, _call_offsets, _calls_fired
    _hour_start   = time.time()
    _call_offsets = sorted(random.uniform(0, 3600) for _ in range(calls_per_hour))
    _calls_fired  = set()
    _call_times = [
        datetime.datetime.fromtimestamp(_hour_start + offset).strftime("%H:%M:%S")
        for offset in _call_offsets
    ]
    print(f"\n⏱️  [{datetime.datetime.now().strftime('%H:%M:%S')}]")
    print(f"[idle] 🕐 New hour scheduled — calls at: {_call_times}")


def _play_ring(path: str) -> subprocess.Popen | None:
    """Start ring audio, return Popen handle or None on error."""
    if not os.path.exists(path):
        print(f"[idle] Audio file not found: {path}")
        return None
    try:
        return subprocess.Popen(
            ["aplay", "-D", AUDIO_CARD_RING, path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        print(f"[idle] Error playing ring: {e}")
        return None


def _check_horn():
    """Non-blocking horn check. Returns 'play_welcome' on lift, else None."""
    if button_horn.is_pressed:
        while button_horn.is_pressed:
            time.sleep(0.01)
        print("\n📞   The horn has been picked up")
        time.sleep(debounce)
        return "play_welcome"
    return None


def _interruptible_sleep(seconds):
    """Sleep in small chunks, returning 'play_welcome' immediately if horn lifted."""
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
    Returns 'play_welcome' if horn is lifted at any point, else None.
    """
    print(f"\n📞 [idle] [{datetime.datetime.now().strftime('%H:%M:%S')}] Incoming call — ringing…")

    for ring_num in range(rings_per_call):
        proc = _play_ring(ring_path)

        if proc:
            while proc.poll() is None:
                result = _check_horn()
                if result:
                    proc.terminate()
                    proc.wait()
                    return result
                time.sleep(0.05)

        if ring_num < rings_per_call - 1:
            result = _interruptible_sleep(ring_interval)
            if result:
                return result

    print("[idle] 📵 Call ended (no answer)")
    return None


# ── Main state entry point ────────────────────────────────────────────────────
def run():
    global _hour_start

    if _hour_start is None:
        _schedule_new_hour()

    if time.time() - _hour_start >= 3600:
        _schedule_new_hour()

    result = _check_horn()
    if result:
        return result

    if ring_on:
        elapsed = time.time() - _hour_start
        for i, offset in enumerate(_call_offsets):
            if i not in _calls_fired and elapsed >= offset:
                _calls_fired.add(i)
                result = _play_call()
                if result:
                    return result

    return None