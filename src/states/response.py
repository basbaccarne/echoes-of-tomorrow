import os
import time
import subprocess
from states.shared import SharedState
import yaml


# ── Config ───────────────────────────────────────────────────────────────────
base_dir  = "/home/pi/echoes-of-tomorrow/src"
audio_dir = "/home/pi/echoes-of-tomorrow/audio_files"

with open(os.path.join(base_dir, "config.yaml"), "r") as f:
    config = yaml.safe_load(f)

AUDIO_CARD = config.get("audio_card", "plughw:0,0")

def _play(path):
    """Play a wav file, return False on error."""
    print(f"\n⏳   Playing {os.path.basename(path)}")
    print("ALSA message:")
    try:
        subprocess.run(["aplay", "-D", AUDIO_CARD, path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"aplay error: {e}")
        return False

def run():
        
    base_dir   = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    booth_id   = SharedState.booth_id
    audio_base = os.path.join(base_dir, "audio_files")

    response_path   = os.path.join(audio_base, f"response_{booth_id}.wav")
    response_0_path = os.path.join(audio_base, f"response_0_{booth_id}.wav")

    print(f"\n⏳   Checking for the response file at {response_path}")

    if not os.path.exists(response_path):
        print("No response file found")
        return "idle"

    print(f"\n⏳   Playing the response for booth ID {booth_id}")

    # Play response_{id}.wav
    if not _play(response_path):
        return "idle"

    # Play response_0_{id}.wav if it exists
    if os.path.exists(response_0_path):
        if not _play(response_0_path):
            return "idle"
    else:
        print(f"   ⚠️  No follow-up file found at {response_0_path}, skipping.")

    print("\n--------------------------------\n")
    print(f"Going back to the idle state.")
    print(f'This device is still set to booth ID: {booth_id}')
    print("👂   Waiting for the horn to be picked up, looking forward to the next conversation ...")
    
    return "idle"