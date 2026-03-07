import os
import time
import subprocess
from hardware import button_horn
from states.shared import SharedState
import yaml

# ── Config ───────────────────────────────────────────────────────────────────
base_dir  = "/home/pi/echoes-of-tomorrow/src"
audio_dir = "/home/pi/echoes-of-tomorrow/audio_files"

with open(os.path.join(base_dir, "config.yaml"), "r") as f:
    config = yaml.safe_load(f)

AUDIO_CARD = config.get("audio_card", "plughw:0,0")
DEBOUNCE = 0.3  # seconds — adjust if needed

def play_audio(audio_path):
    """Play an audio file, return 'interrupted' if horn is replaced, else None."""
    try:
        process = subprocess.Popen([
            "aplay",
            "-D", AUDIO_CARD,
            audio_path
        ])

        while process.poll() is None:
            if button_horn.is_pressed:
                print("Horn replaced — returning to idle.")
                process.terminate()
                return "interrupted"
            time.sleep(0.1)

        if process.returncode != 0:
            print(f"aplay exited with code {process.returncode}")
            return "error"

    except Exception as e:
        print(f"aplay error: {e}")
        return "error"

    return None


def run():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    pickup_path  = os.path.join(base_dir, "audio_files", "pick-up_phone.wav")
    welcome_path = os.path.join(base_dir, "audio_files", f"welcome_{SharedState.booth_id}.wav")

    time.sleep(DEBOUNCE)

    # ── 1. Play pick-up sound ─────────────────────────────────────────────────
    print("🔔  Playing pick-up sound...")
    result = play_audio(pickup_path)
    if result in ("interrupted", "error"):
        return "idle"

    # ── 2. Play welcome message ───────────────────────────────────────────────
    print(f"\n🗣️   Playing the welcome message of the librarian 👴")
    print("ALSA message:")
    result = play_audio(welcome_path)
    if result in ("interrupted", "error"):
        return "idle"

    print("Welcome message finished.")
    return "recording"