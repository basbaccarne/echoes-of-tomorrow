import time
import datetime
from states.shared import SharedState
from pathlib import Path
import yaml
import os
import warnings
from faster_whisper import WhisperModel

# Directories
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.yaml"

# Settings
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)
SAVE_DIR = config["audio_path"]
os.makedirs(SAVE_DIR, exist_ok=True)

#it would be good if the model only needs to be loaded once, not with every transcription.
print("Loading faster-whisper model...")
load_start = time.time()
model = WhisperModel(
    "small", 
    device="cpu",
    compute_type="int8"
)
load_time = time.time() - load_start
print(f"✓ Model loaded in {load_time:.2f} seconds!")

def process_audio(path_in, model):
    print(f"Transcribing: {path_in}")

    transcribe_start = time.time()
    
    segments, info = model.transcribe(
        path_in,
        language="nl",
        beam_size=1,
        vad_filter=False,
        without_timestamps=True
    )
    
    print("Processing segments...")
    segments_list = list(segments)
    
    transcribe_time = time.time() - transcribe_start
    
    print(f"Found {len(segments_list)} segments")
    print(f"⏱️  Transcription took {transcribe_time:.2f} seconds")
    
    text = " ".join([segment.text for segment in segments_list])
    
    print("✓ Transcription complete!")

    # Build output file path
    filename = os.path.splitext(os.path.basename(path_in))[0]
    path_out = os.path.join(os.path.dirname(path_in), f"{filename}.txt")

    with open(path_out, "w", encoding="utf-8") as f:
        f.write(text)

    return text

def run():
    print(f"Audio file that needs to be transformed to text: question_{SharedState.booth_id}.wav")
    audio_path = SAVE_DIR
    print(f"in directory: {audio_path}")
    # get the WAV from audio_files/question_0.wav (where 0 is the booth id, to be set in config.yaml)
    # transform the WAV file to text
    # store in audio_files/question_0.txt (where 0 is the booth id, to be set in config.yaml)
    input_path = os.path.join(audio_path, f"/question_{SharedState.booth_id}.wav")
    response = process_audio(input_path, model)
    #time.sleep(5)  # simulate processing time
    #response  = "this the the spoken word i tried to get from the audio, but it can be anything, it's just a placeholder for now"
    print(f"Text response should be stored in: question_{SharedState.booth_id}.txt")
    print(f"in directory: {audio_path}")

    print(f"\n⏱️  [{(datetime.datetime.now().strftime('%H:%M:%S'))}]") 
    print("🎙️  I've transformed the wav to text.")
    print(f"📜  Here's the transcript: {response}")
    print("\nSending transcript to n8n for further processing...")

    return "n8n"