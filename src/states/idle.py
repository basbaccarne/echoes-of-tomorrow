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

# 🔧 TEST MODE SWITCH
testing = True  # True = trigger in 30s, False = random within hour


# ── Scheduler ─────────────────────────────────────────────────────────────
def _schedule_new_hour():
    now = time.time()

    SharedState.idle_hour_start = now

    if testing:
        SharedState.idle_trigger_time = now + 30
        print("\n🧪 TEST MODE ENABLED")
    else:
        SharedState.idle_trigger_time = now + random.uniform(0, 3600)

    SharedState.triggered_this_hour = False

    print(f"\n⏱️ [{datetime.datetime.now().strftime('%H:%M:%S')}]")
    print(
        "[idle] next trigger at:",
        datetime.datetime.fromtimestamp(SharedState.idle_trigger_time).strftime("%H:%M:%S")
    )


# ── Audio ────────────────────────────────────────────────────────────────
def _play_ring(path: str):
    if not os.path.exists(path):
        print(f"[idle] ❌ Missing audio: {path}")
        return None

    print(f"[idle] 🔊 playing ring")

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
    end = time.time() + seconds

    while time.time() < end:
        result = _check_horn()
        if result:
            return result
        time.sleep(0.05)

    return None


# ── Call logic (4 rings) ─────────────────────────────────────────────────
def _play_call():

    print(f"\n📞 Incoming call — {rings_per_call} rings")

    for i in range(rings_per_call):

        print(f"[idle] 🔔 Ring {i + 1}/{rings_per_call}")

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
            print("[idle] ⏳ waiting between rings")
            result = _interruptible_sleep(ring_interval)
            if result:
                return result

    print("[idle] 📵 Call ended")
    return None


# ── Main entry point ─────────────────────────────────────────────────────
def run():

    # init
    if SharedState.idle_hour_start is None:
        _schedule_new_hour()

    now = time.time()

    # hourly reset
    if now - SharedState.idle_hour_start >= 3600:
        _schedule_new_hour()

    # horn always wins
    result = _check_horn()
    if result:
        return result

    # trigger logic (SIMPLE + SAFE)
    if (not SharedState.triggered_this_hour and
            now >= SharedState.idle_trigger_time):

        SharedState.triggered_this_hour = True

        print(f"\n📞 TRIGGERED at {datetime.datetime.now()}")

        return _play_call()

    return None