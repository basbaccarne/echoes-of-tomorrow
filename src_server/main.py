# main state machine of the server
# quickest hack is to run this script for each pi on a different port
# to each pi sends to another port, so we can run 4 paralllel state machines on the same server

# run using "python main.py --booth-id=0" (or 1, 2, 3)

# static config is stored in config.yaml
# dynamic config is stored in states/shared.py (SharedState class)

import importlib
import time
import argparse
from states.shared import SharedState
from faster_whisper import WhisperModel
from pathlib import Path
import yaml
from piper import PiperVoice

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--booth-id", type=int, required=True)
args = parser.parse_args()

# load config
BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.yaml"
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# set shared state
SharedState.booth_id = args.booth_id

# welcome message
print("\n---------------------------------")
print(f"🚀 Starting server for booth ID {SharedState.booth_id}...\n")

# preload whisper
print("👂 Loading faster-whisper speech-to-text model...")
load_start = time.time()
SharedState.whisper_model = WhisperModel("small", device="cpu", compute_type="int8")
print(f"✓ Model loaded in {time.time() - load_start:.2f} seconds!\n")

# preload piper voices
print(f"💬 Loading piper voice model [ID {SharedState.booth_id}]...")
load_start = time.time()
voice_path = Path(config["voice_path"][SharedState.booth_id])
SharedState.piper_voice = PiperVoice.load(voice_path)
print(f"✓ Piper voice loaded in {time.time() - load_start:.2f} seconds!")

print("\n✓ Server started... \n")

state = "waiting_for_receive"
# for testing: uncomment the line below and change with the state you want to start from
# state = "stt"

loaded_state = None
last_sender_ip = None

try:
    while True:
        try:
            # load module only when state changes
            if loaded_state != state:
                module = importlib.import_module(f"states.{state}")
                importlib.reload(module)
                loaded_state = state

            # run state (module always exists after load)
            next_state = module.run()

            if next_state and next_state != state:
                print(f"\n➡️  Switching to state: {next_state}")
                state = next_state

        except Exception as e:
            print(f"Error in state {state}: {e}")
            state = "waiting_for_receive"

        time.sleep(0.01)

except KeyboardInterrupt:
    print("Program stopped by user")