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

    # IMPORTANT: store ONLY timestamps (floats)
    SharedState.idle_call_times = sorted(
        now + random.uniform(0, 3600)
        for _ in range(calls_per_hour)
    )

    SharedState.idle_calls_fired = set()

    print(f"\n⏱️  [{datetime.datetime.now().strftime('%H:%M:%S')}]")
    print("[idle] 🕐 New hour scheduled — calls at:")

    for t in SharedState.idle_call_times:
        print("   -", datetime.datetime.fromtimestamp(t).strftime("%H:%M:%S"))


# ── Audio ────────────────────────────────────────────────────────────────
def _play_ring(path: str):
    if not os.path.exists(path):
        print(f"[idle] ❌ Audio file not found: {path}")
        return None

    print(f"[idle] 🔊 playing ring: {path}")

    try:
        return subprocess.Popen(
            ["aplay", "-D", AUDIO_CARD_RING, path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        print(f"[idle] ❌ aplay error: {e}")
        return None


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
    end = time.time() + seconds

    while time.time() < end:
        result = _check_horn()
        if result:
            return result
        time.sleep(0.05)

    return None


# ── Call logic ───────────────────────────────────────────────────────────
def _play_call():
    print(f"\n📞 [{datetime.datetime.now().strftime('%H:%M:%S')}] Incoming call — ringing…")

    for i in range(rings_per_call):

        proc = _play_ring(ring_path)

        if proc:
            while proc.poll() is None:
                result = _check_horn()
                if result:
                    proc.terminate()
                    proc.wait()
                    return result
                time.sleep(0.05)

        if i < rings_per_call - 1:
            result = _interruptible_sleep(ring_interval)
            if result:
                return result

    print("[idle] 📵 Call ended (no answer)")
    return None


# ── Main entry point ─────────────────────────────────────────────────────
def run():
    
    print(f"[DEBUG] call_times exists: {hasattr(SharedState, 'idle_call_times')}")
    print(f"[DEBUG] call_times value: {getattr(SharedState, 'idle_call_times', None)}")
    print(f"[DEBUG] fired: {getattr(SharedState, 'idle_calls_fired', None)}")

    # ensure scheduler exists
    if not hasattr(SharedState, "idle_call_times") or not SharedState.idle_call_times:
        _schedule_new_hour()

    if SharedState.idle_hour_start is None:
        _schedule_new_hour()

    # hourly reset
    if time.time() - SharedState.idle_hour_start >= 3600:
        _schedule_new_hour()

    # horn check
    result = _check_horn()
    if result:
        return result

    if ring_on:
        now = time.time()

        for i, call_time in enumerate(SharedState.idle_call_times):

            # DEBUG (keep this until stable)
            # print(f"[DEBUG] now={now}, call_time={call_time}")

            if i in SharedState.idle_calls_fired:
                continue

            if now >= call_time:
                print(
                    f"\n📞 triggering call {i} "
                    f"({datetime.datetime.fromtimestamp(call_time).strftime('%H:%M:%S')})"
                )

                SharedState.idle_calls_fired.add(i)

                result = _play_call()
                if result:
                    return result

    return None