import time
import datetime
import requests
import os
from pathlib import Path
import yaml
from states.shared import SharedState

# Directories
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.yaml"

# Settings
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

SEND_DIR = config["audio_path"]

# Main variables
filename = f"response_{config['booth_id']}.wav"
filepath = os.path.join(SEND_DIR, filename)

port = config["unique_port"].get(SharedState.booth_id, PORT)
booth_ip = config["booth_ip"].get(config["booth_id"])


def run():
    # print info about file and destination (single log)
    print("\nsending file:", filepath, "-> to ip:", booth_ip, " over port:", port)

    # helper function to send wav file (with error handling)
    def send_wav(filepath, server_ip, port):
        filename = os.path.basename(filepath)

        try:
            with open(filepath, "rb") as f:
                response = requests.post(
                    f"http://{server_ip}:{port}/upload",
                    data=f,
                    headers={
                        "Content-Type": "audio/wav",
                        "X-Filename": filename
                    },
                    timeout=5  # avoid hanging forever
                )

            return response.ok

        except requests.exceptions.ConnectTimeout:
            print("❌ Server timeout (not reachable)")
            return False

        except requests.exceptions.ConnectionError:
            print("❌ Server unavailable (connection error)")
            return False

        except Exception as e:
            print(f"❌ Unexpected send error: {e}")
            return False

    # 1. Wait until file exists
    if not os.path.exists(filepath):
        print(f"⏳ File not found (yet): {filepath}")
        return "sending"  # stay in same state

    # 2. Try to send (network-safe)
    try:
        success = send_wav(filepath, booth_ip, port)
    except Exception as e:
        print(f"❌ Send error: {e}")
        time.sleep(2)
        return "sending"

    # 3. Handle result
    if success:
        print(f"\n⏱️ [{datetime.datetime.now().strftime('%H:%M:%S')}]")
        print("📤 Audiofile sent successfully.")
        return "waiting_for_receive"

    # 4. If server returned error, retry
    print("❌ Server rejected file or not reachable, retrying...")
    time.sleep(2)
    return "sending"