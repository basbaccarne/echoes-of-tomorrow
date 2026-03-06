import time
import datetime
import requests
from states.shared import SharedState
from pathlib import Path
import yaml
import os

# WEBHOOKS
#Tims hook
#url = "http://localhost:5678/webhook/dae1d29b-5725-47fc-a68b-cba9d669a981/chat"
#local test
# url = "http://localhost:5678/webhook/4a373672-3af4-4cae-a776-67fe0c43a3e6/chat" 
#SSH test
url = "http://localhost:5678/webhook/70f7a510-eec9-410d-b623-de8bc323273a/chat"

TIMEOUT = 60  # wait up to 60s

# Directories
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.yaml"

# Settings
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)
SAVE_DIR = config["audio_path"]
os.makedirs(SAVE_DIR, exist_ok=True)


def send_to_n8n(text):
    payload = {"chatInput": text}
    response = requests.post(url, json=payload, timeout=TIMEOUT)
    response.raise_for_status()
    print(f"✓ Sent to n8n (status {response.status_code})\n\nWaiting for response...\n")
    # try JSON first, fall back to plain text
    try:
        data = response.json()
        return data.get("output") or data.get("text") or (data.get("message") or {}).get("content") or str(data)
    except Exception:
        return response.text


def run():
    # print(f"Text file that needs to be added to the webhook is: question_{SharedState.booth_id}.txt")
    # print(f"in directory: {SAVE_DIR}")

    # Read the transcript from the .txt file written by stt.py
    input_path = os.path.join(SAVE_DIR, f"question_{SharedState.booth_id}.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        question_text = f.read()

    # Send to n8n and wait for response
    print(f"💬 Sending question to n8n: \n{question_text}")
    response = send_to_n8n(question_text)

    # Store response in .txt file
    output_path = os.path.join(SAVE_DIR, f"response_{SharedState.booth_id}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response)

    # print(f"The text file of the agent response needs to be stored in: response_{SharedState.booth_id}.txt")
    # print(f"in directory: {SAVE_DIR}")

    print(f"⏱️  [{datetime.datetime.now().strftime('%H:%M:%S')}]")
    print("🤖 Agent response ready.")
    print(f"💬 This is the reply: \n{response}")
    # print("\nSending this text to the text to speech module...")

    return "tts"