import time
import datetime
from states.shared import SharedState
from pathlib import Path
import yaml
import os
import wave
from piper import PiperVoice, SynthesisConfig

# Directories
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.yaml"

# Settings
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)
VOICE_PATHS = config["voice_path"]
SAVE_DIR = config["audio_path"]
os.makedirs(SAVE_DIR, exist_ok=True)

def process_text(path_in, voice, speed=1.0):
       
    speed_inv = 1/speed

    with open(path_in, 'r') as file:
        txtinput = file.read().replace('\n', '')

    print(f"🔊 Speaking (speed {speed_inv}x): {txtinput[:50]}...")
    t1 = time.time()

    syn_config = SynthesisConfig(
        volume=0.5,  # half as loud
        length_scale=speed_inv,  # speed_inv times as slow
        noise_scale=1.0,  # more audio variation
        noise_w_scale=1.0,  # more speaking variation
        normalize_audio=False, # use raw audio from voice
    )

    # Build output file path
    filename = os.path.splitext(os.path.basename(path_in))[0]
    file_out = os.path.join(os.path.dirname(path_in), f"{filename}.wav")

    with wave.open(file_out, "wb") as wav_file:
        voice.synthesize_wav(txtinput, wav_file, syn_config= syn_config)

    t2 = time.time()
    print(f"⏱️  Generated in {t2-t1:.2f}s")

    return t2-t1

def run():
    
    text_path = SAVE_DIR
    print(f"Text file that needs to be transformed to WAV in: response_{SharedState.booth_id}.txt")
    print(f"in directory: {text_path}")
    
    # get the reponse text from audio_files/response_0.txt (where 0 is the booth id, to be set in config.yaml)
    # transform txt to WAV file
    # store in audio_files/response_0.wav (where 0 is the booth id, to be set in config.yaml)
    voice_path = Path(VOICE_PATHS[SharedState.booth_id])
    v = PiperVoice.load(voice_path)
    input_path = os.path.join(text_path, f"response_{SharedState.booth_id}.txt")
    response = process_text(input_path, v)
    print(f"The WAV file should be stored as: response_{SharedState.booth_id}.wav")
    print(f"in directory: {text_path}")
        
    print(f"\n⏱️  [{(datetime.datetime.now().strftime('%H:%M:%S'))}]") 
    print("🔊 Audio file ready.")
    print("Sending this back to the pi...")

    return "sending"