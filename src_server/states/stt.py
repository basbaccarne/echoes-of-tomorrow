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


def process_audio(path_in, model):
    # print(f"Transcribing: {path_in}")

    transcribe_start = time.time()

    segments, info = model.transcribe(
        path_in,
        language="nl",
        beam_size=1,
        vad_filter=False,
        without_timestamps=True
    )

    # print("Processing segments...")
    segments_list = list(segments)

    transcribe_time = time.time() - transcribe_start
    # print(f"Found {len(segments_list)} segments")
    # print(f"⏱️  Transcription took {transcribe_time:.2f} seconds")

    text = " ".join([segment.text for segment in segments_list])
    print(f"✓ Transcription complete in {transcribe_time:.2f} seconds!")

    # Write output .txt next to the input .wav
    filename = os.path.splitext(os.path.basename(path_in))[0]
    dir_name = os.path.dirname(path_in)
    path_out = os.path.join(dir_name, f"{filename}.txt")

    with open(path_out, "w", encoding="utf-8") as f:
        f.write(text)

    return text


def run():
    model = SharedState.whisper_model
    if model is None:
        raise RuntimeError("Whisper model not loaded — ensure main.py initialized SharedState.whisper_model")

    audio_path = SAVE_DIR
    input_path = os.path.join(SAVE_DIR, f"question_{SharedState.booth_id}.wav")

    print(f"📜 transcribing question_{SharedState.booth_id}.wav")
    # print(f"In directory: {audio_path}")

    response = process_audio(input_path, model)

    # print(f"Text response stored in: question_{SharedState.booth_id}.txt")
    # print(f"In directory: {audio_path}")
    print(f"\n⏱️  [{datetime.datetime.now().strftime('%H:%M:%S')}]")
    # print("🎙️  I've transformed the wav to text.")
    print(f"📜  Transcript:{response}")
    # print("\nSending transcript to n8n for further processing...")

    return "n8n"