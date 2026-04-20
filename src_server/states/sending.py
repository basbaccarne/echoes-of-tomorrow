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


def run():
    # ── Resolve per-session values inside run() ───────────────────────────────
    booth_id = SharedState.booth_id
    port     = config["unique_port"].get(booth_id, 8765)
    filename = f"response_{booth_id}.wav"
    filepath = os.path.join(SEND_DIR, filename)
    booth_ip = SharedState.sender_ip or config["booth_ip"].get(booth_id, "127.0.0.1")

    print(f"\n⌲ sending {filename} back to {booth_ip} over port {port}")

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
                    timeout=5
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
        return "sending"

    # 2. Try to send (network-safe)
    try:
        success = send_wav(filepath, booth_ip, port)
    except Exception as e:
        print(f"❌ Send error: {e}")
        time.sleep(2)
        return "sending"

    # 3. Handle result
    if success:
        print("✓ Audiofile sent successfully.")
        return "waiting_for_receive"

    # 4. If server returned error, retry
    print("❌ Server rejected file or not reachable, retrying...")
    time.sleep(2)
    return "sending"