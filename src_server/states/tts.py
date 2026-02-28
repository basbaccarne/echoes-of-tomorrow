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
    
    audio_path = SAVE_DIR
    print(f"Text file that needs to be transformed to WAV in: response_{SharedState.booth_id}.txt")
    print(f"in directory: {audio_path}")
    
    # get the reponse text from audio_files/response_0.txt (where 0 is the booth id, to be set in config.yaml)
    # transform txt to WAV file
    # store in audio_files/response_0.wav (where 0 is the booth id, to be set in config.yaml)
    
    time.sleep(5)  # simulate processing time
    
    audio_path = SAVE_DIR
    print(f"The WAV file should be stored as: response_{SharedState.booth_id}.wav")
    print(f"in directory: {audio_path}")
        
    print(f"\n⏱️  [{(datetime.datetime.now().strftime('%H:%M:%S'))}]") 
    print("🔊 Audio file ready.")
    print("Sending this back to the pi...")

    return "sending"