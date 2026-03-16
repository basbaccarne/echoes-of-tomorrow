import os
import time
import subprocess

from hardware import button_horn
from shared import AUDIO_CARD, SharedState

# ── Config ────────────────────────────────────────────────────────────────────
audio_dir = "/home/pi/echoes-of-tomorrow/audio_files"
DEBOUNCE  = 0.3


def _play_audio(path: str) -> str | None:
    """Play an audio file on the default (USB) card.
    
    Returns:
        'interrupted' if horn is replaced mid-play
        'error'       if the file is missing or aplay fails
        None          on clean completion
    """
    if not os.path.exists(path):
        print(f"[play_welcome] Audio file not found: {path}")
        return "error"

    try:
        proc = subprocess.Popen(
            ["aplay", "-D", AUDIO_CARD, path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        while proc.poll() is None:
            if button_horn.is_pressed:
                print("[play_welcome] Horn replaced — returning to idle.")
                proc.terminate()
                proc.wait()
                return "interrupted"
            time.sleep(0.05)

        if proc.returncode != 0:
            print(f"[play_welcome] aplay exited with code {proc.returncode}")
            return "error"

    except Exception as e:
        print(f"[play_welcome] aplay error: {e}")
        return "error"

    return None


def run():
    pickup_path  = os.path.join(audio_dir, "pick-up_phone.wav")
    welcome_path = os.path.join(audio_dir, f"welcome_{SharedState.booth_id}.wav")

    time.sleep(DEBOUNCE)

    # ── 1. Play pick-up sound ─────────────────────────────────────────────────
    print("[play_welcome] 🔔  Playing pick-up sound...")
    if _play_audio(pickup_path) is not None:
        return "idle"

    # ── 2. Play welcome message ───────────────────────────────────────────────
    print(f"[play_welcome] 🗣️  Playing welcome message for booth {SharedState.booth_id}...")
    if _play_audio(welcome_path) is not None:
        return "idle"

    print("[play_welcome] ✅  Welcome message finished.")
    return "recording"