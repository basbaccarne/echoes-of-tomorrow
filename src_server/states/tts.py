import time
import datetime
from states.shared import SharedState
from pathlib import Path
import yaml
import os
import wave
from piper import SynthesisConfig

# Directories
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.yaml"

# Settings
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)
SAVE_DIR = Path(config["audio_path"])
os.makedirs(SAVE_DIR, exist_ok=True)

tts_start = time.time()

def process_text(path_in, voice, speed=0.8):
       
    speed_inv = 1/speed
    path_in = Path(path_in)
    
    with open(path_in, 'r') as file:
        txtinput = file.read().replace('\n', '')

    print("\n🔊 Transforming text to speech with Piper...")
    # print(f"Settings: speed = {speed_inv}x -: {txtinput[:50]}...")
    t1 = time.time()

    syn_config = SynthesisConfig(
        volume=1,  # half as loud
        length_scale=speed_inv,  # speed_inv times as slow
        noise_scale=0.8,  # more audio variation
        noise_w_scale=1.0,  # more speaking variation
        normalize_audio=False, # use raw audio from voice
    )

    # Build output file path
    file_out = path_in.with_suffix(".wav")

    with wave.open(str(file_out), "wb") as wav_file:
        voice.synthesize_wav(txtinput, wav_file, syn_config= syn_config)

    elapsed = time.time() - t1
    # print(f"\n⏱️  Generated in {elapsed:.2f}s")

    return elapsed

def run():
    
    input_path = SAVE_DIR / f"response_{SharedState.booth_id}.txt"
    
    # print(f"Text file that needs to be transformed to WAV: {input_path.name}")
    # print(f"in directory: {SAVE_DIR}")
    
    v = SharedState.piper_voice  # preloaded in main.py
    v = SharedState.piper_voice  # preloaded in main.py
    voice_name = Path(config["voice_path"][SharedState.booth_id]).name
    print(f"🗣️  Voice model: {voice_name}")
    elapsed = process_text(input_path, v)
    
    # print(f"Stored as: response_{SharedState.booth_id}.wav")
    # print(f"in directory: {SAVE_DIR}")
    tts_time = time.time() - tts_start
    print(f"✓ WAV file generated in {tts_time:.2f} seconds!")
    print(f"\n⏱️  [{datetime.datetime.now().strftime('%d/%m %H:%M:%S')}]")
    print("🔊 Audio file ready. Sending this back to the pi...")
    
    # general timer:
    # [!] move to sending once complete
    session_time = time.time() - SharedState.session_start
    print(f"\n🏁🏁 ⏱️ Total server processing time: {session_time:.2f} seconds!⏱️ 🏁🏁")

    return "sending"