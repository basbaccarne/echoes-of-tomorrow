import importlib
import time
import argparse
from states.shared import SharedState
from faster_whisper import WhisperModel
from pathlib import Path
import yaml
from piper import PiperVoice
import torch

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

# detect device
if torch.cuda.is_available():
    device = "cuda"
    compute_type = "float16"
    print(f"🖥️  GPU detected: {torch.cuda.get_device_name(0)}")
else:
    device = "cpu"
    compute_type = "int8_float32"
    print("🖥️  No GPU detected, falling back to CPU")

# preload whisper
print("👂 Loading faster-whisper speech-to-text model...")
load_start = time.time()
SharedState.whisper_model = WhisperModel(
    "medium",
    device=device,
    compute_type=compute_type,
    cpu_threads=4,   # ignored on GPU; tune to core count / num booths on CPU
    num_workers=1,
)
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