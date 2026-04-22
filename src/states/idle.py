import time
import datetime
import os
import random
import subprocess

from hardware import button_horn
from states.shared import SharedState, AUDIO_CARD_RING

# ── Config ────────────────────────────────────────────────────────────────
audio_dir = "/home/pi/echoes-of-tomorrow/audio_files"
ring_path = os.path.join(audio_dir, "ring.wav")
debounce = 0.3

ring_on = True

rings_per_call = 4
ring_interval = 2
calls_per_hour = 50


# ── Scheduler ──────────────────────────────────────────────────────────────
def _schedule_new_hour():
    now = time.time()

    SharedState.idle_hour_start = now

    SharedState.idle_call_times = sorted(
        now + random.uniform(0, 3600)
        for _ in range(calls_per_hour)
    )

    SharedState.idle_calls_fired = set()

    _call_times = [
        datetime.datetime.fromtimestamp(t).strftime("%H:%M:%S")
        for t in SharedState.idle_call_times
    ]

    print(f"\n⏱️  [{datetime.datetime.now().strftime('%H:%M:%S')}]")
    print(f"[idle] 🕐 New hour scheduled — calls at: {_call_times}")


# ── Audio ────────────────────────────────────────────────────────────────
def _play_ring(path: str):
    if not os.path.exists(path):
        print(f"[idle] Audio file not found: {path}")
        return None

    print(f"[idle] ▶ playing ring: {path}")

    return subprocess.Popen(
        ["aplay", "-D", AUDIO_CARD_RING, path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


# ── Input ────────────────────────────────────────────────────────────────
def _check_horn():
    if button_horn.is_pressed:
        while button_horn.is_pressed:
            time.sleep(0.01)

        print("\n📞 Horn picked up")
        time.sleep(debounce)

        _schedule_new_hour()
        return "play_welcome"

    return None


def _interruptible_sleep(seconds):
    deadline = time.time() + seconds

    while time.time() < deadline:
        result = _check_horn()
        if result:
            return result
        time.sleep(0.05)

    return None


# ── Call Logic ───────────────────────────────────────────────────────────
def _play_call():
    print(f"\n📞 [{datetime.datetime.now().strftime('%H:%M:%S')}] Incoming call — ringing…")

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


# ── Main state entry point ───────────────────────────────────────────────
def run():

    # Ensure scheduler exists
    if not hasattr(SharedState, "idle_call_times"):
        _schedule_new_hour()

    if SharedState.idle_hour_start is None:
        _schedule_new_hour()

    # hourly reset safety
    if time.time() - SharedState.idle_hour_start >= 3600:
        _schedule_new_hour()

    # horn check
    result = _check_horn()
    if result:
        return result

    # trigger calls
    if ring_on:
        now = time.time()

        for i, call_time in enumerate(SharedState.idle_call_times):

            if i in SharedState.idle_calls_fired:
                continue

            if now >= call_time:
                print(f"\n📞 triggering call {i} at {datetime.datetime.now()}")
                SharedState.idle_calls_fired.add(i)

                result = _play_call()
                if result:
                    return result

    return None