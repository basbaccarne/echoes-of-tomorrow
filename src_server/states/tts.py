import time
import datetime
import sys
from pathlib import Path
from states.shared import SharedState
import yaml
import os

# Directories
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.yaml"

# Settings
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)
SAVE_DIR = Path(config["audio_path"])
os.makedirs(SAVE_DIR, exist_ok=True)

# TTS backends live in tests/TTS as standalone importable modules
_TESTS_TTS = BASE_DIR.parent / "tests" / "TTS"
sys.path.insert(0, str(_TESTS_TTS))
from elevenlabs_test import text_to_speech as _elevenlabs_tts
from piper_tts import text_to_speech as _piper_tts

tts_start = time.time()


def run():

    input_path = SAVE_DIR / f"response_{SharedState.booth_id}.txt"
    output_path = str(input_path.with_suffix(".wav"))

    with open(input_path, "r") as f:
        text = f.read().replace("\n", "")

    # Try ElevenLabs first, fall back to Piper on any failure
    voice_id = config["elevenlabs_voice_id"][SharedState.booth_id]
    print(f"[TTS] Trying ElevenLabs (voice: {voice_id})...")
    try:
        _elevenlabs_tts(text, output_path, voice_id=voice_id)
        print("[TTS] ElevenLabs succeeded")
    except Exception as e:
        print(f"[TTS] ElevenLabs failed: {e}")
        print("[TTS] Falling back to Piper...")
        voice_name = Path(config["voice_path"][SharedState.booth_id]).name
        print(f"[TTS] Piper voice: {voice_name}")
        _piper_tts(text, output_path, SharedState.piper_voice)

    tts_time = time.time() - tts_start
    print(f"✓ WAV file generated in {tts_time:.2f} seconds!")
    print(f"\n⏱️  [{datetime.datetime.now().strftime('%d/%m %H:%M:%S')}]")
    print("🔊 Audio file ready. Sending this back to the pi...")

    session_time = time.time() - SharedState.session_start
    print(f"\n🏁🏁 ⏱️ Total server processing time: {session_time:.2f} seconds!⏱️ 🏁🏁")

    return "sending"
