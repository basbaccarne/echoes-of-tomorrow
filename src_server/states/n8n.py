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
    
    print(f"Text file that needs to be added to the webhook is: question_{SharedState.booth_id}.txt")
    audio_path = SAVE_DIR
    print(f"in directory: {audio_path}")

    # get the question text from audio_files/question_0.txt (where 0 is the booth id, to be set in config.yaml)
    # send a webhook to n8n
    # wait for the reponse (while loop)
    # store in audio_files/response_0.txt (where 0 is the booth id, to be set in config.yaml)

    
    time.sleep(5)  # simulate processing time
    
    response  = "this the reponse from n8n, but it can be anything, it's just a placeholder for now"
    
    audio_path = SAVE_DIR
    
    print(f"The text file of the agent response needs to be stored in: response_{SharedState.booth_id}.txt")
    print(f"in directory: {audio_path}")


    print(f"\n⏱️  [{(datetime.datetime.now().strftime('%H:%M:%S'))}]") 
    print("🤖 Agent response ready.")
    print(f"💬 Here's the reply: {response}")
    print("\nSending this text to the text to speech module...")
    return "tts"