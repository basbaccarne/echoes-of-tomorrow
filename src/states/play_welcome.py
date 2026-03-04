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

def run():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    audio_path = os.path.join(base_dir, "audio_files", f"welcome_{SharedState.booth_id}.wav")

    print(f"\n🗣️   Playing the welcome message of the librarian 👴")
    print("ALSA message:")

    # Wait briefly before monitoring the horn so we don't catch
    # the tail end of the pickup gesture triggering is_pressed = False
    time.sleep(DEBOUNCE)

    try:
        process = subprocess.Popen([
            "aplay",
            "-D", AUDIO_CARD,
            audio_path
        ])

        while process.poll() is None:
            if button_horn.is_pressed:   # horn put back down = on the hook
                print("Horn replaced during welcome — returning to idle.")
                process.terminate()
                return "idle"
            time.sleep(0.1)

        if process.returncode != 0:
            print(f"aplay exited with code {process.returncode}")
            return "idle"

    except Exception as e:
        print(f"aplay error: {e}")
        return "idle"

    print("Welcome message finished.")
    return "recording"