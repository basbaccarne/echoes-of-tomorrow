import time
import datetime
from states.shared import SharedState
from pathlib import Path
import yaml
import os

# Directories
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.yaml"

# Settings
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)
SAVE_DIR = config["audio_path"]
os.makedirs(SAVE_DIR, exist_ok=True)

def run():
    
    print(f"Audio file that needs to be transformed to text: question_{SharedState.booth_id}.wav")
    audio_path = SAVE_DIR
    print(f"in directory: {audio_path}")
    # get the WAV from audio_files/question_0.wav (where 0 is the booth id, to be set in config.yaml)
    # transform to WAV file to text
    # store in audio_files/question_0.txt (where 0 is the booth id, to be set in config.yaml)
    
    time.sleep(5)  # simulate processing time
    response  = "this the the spoken word i tried to get from the audio, but it can be anything, it's just a placeholder for now"
    print(f"Text response should be stored in: question_{SharedState.booth_id}.txt")
    print(f"in directory: {audio_path}")

    print(f"\n⏱️  [{(datetime.datetime.now().strftime('%H:%M:%S'))}]") 
    print("🎙️  I've transformed the wav to text.")
    print(f"📜  Here's the transcript: {response}")
    print("\nSending transcript to n8n for further processing...")

    return "n8n"