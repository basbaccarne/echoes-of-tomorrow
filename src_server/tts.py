"""
╔══════════════════════════════════════════════════════════════╗
║              🔊  PIPER TEXT-TO-SPEECH GENERATOR              ║
║                  Standalone script — easy to use!            ║
╚══════════════════════════════════════════════════════════════╝

REQUIREMENTS:
    pip install piper-tts

PIPER VOICES:
    0 → nl_BE-rdh-medium      (male)
    1 → nl_BE-nathalie-medium (female)
    Set VOICE_CHOICE below to 0 or 1.

USAGE:
    python piper_tts.py
"""

# ─────────────────────────────────────────────
#  ⚙️  SETTINGS — edit these to your liking
# ─────────────────────────────────────────────

# 📝 Input: type your text directly here, or point to a .txt file.
#    If TEXT_INPUT is set, it takes priority over INPUT_FILE.
TEXT_INPUT = """
Hello! This is a test of the Piper text-to-speech system.
You can replace this text with anything you like.
"""

# 💾 Where to save the generated audio file
import os as _os
OUTPUT_FILE = _os.path.join(_os.path.expanduser("~"), "Desktop", "output.wav")

# 🗣️  Choose a voice — set VOICE_CHOICE to 0 or 1
#
#   0 → nl_BE-rdh-medium      (male)
#   1 → nl_BE-nathalie-medium (female)
#
VOICE_CHOICE = 0   # ← change this to 0 or 1

_VOICES = {
    0: "/home/io/echoes-of-tomorrow/src_server/voices/nl_BE-rdh-medium.onnx",
    1: "/home/io/echoes-of-tomorrow/src_server/voices/nl_BE-nathalie-medium.onnx",
}
VOICE_MODEL_PATH = _VOICES[VOICE_CHOICE]

# ⚡ Speed of speech
#    1.0 = normal | < 1.0 = faster | > 1.0 = slower
#    Recommended range: 0.7 (fast) → 1.5 (slow)
SPEED = 1.0

# 🔊 Volume multiplier
#    1.0 = normal | 0.5 = half volume | 2.0 = double volume
VOLUME = 1.0

# 🎲 Audio variation — how much the audio texture varies
#    0.0 = robotic/flat | 1.0 = natural | 2.0 = very varied
NOISE_SCALE = 0.667

# 🎤 Speaking variation — how much the rhythm/timing varies
#    0.0 = very steady | 1.0 = natural variation
NOISE_W_SCALE = 0.8

# 📊 Normalize audio levels before saving?
#    True = auto-level the output | False = raw audio from voice model
NORMALIZE_AUDIO = False

# ─────────────────────────────────────────────
#  🚀  SCRIPT — no need to edit below this line
# ─────────────────────────────────────────────

import time
import datetime
import wave
from pathlib import Path


def load_text() -> str:
    """Return the text to synthesize."""
    text = TEXT_INPUT.strip()
    if not text:
        raise ValueError("TEXT_INPUT is empty — add some text at the top of the script.")
    return text


def load_voice():
    """Load the Piper voice model."""
    try:
        from piper import PiperVoice
    except ImportError:
        raise ImportError(
            "Piper is not installed. Run:  pip install piper-tts"
        )

    model_path = Path(VOICE_MODEL_PATH)
    if not model_path.exists():
        raise FileNotFoundError(
            f"Voice model not found: {VOICE_MODEL_PATH}\n"
            "Check that the path is correct and the file exists on this machine."
        )

    print(f"🗣️  Loading voice model: {model_path.name}")
    return PiperVoice.load(str(model_path))


def synthesize(text: str, voice) -> float:
    """Synthesize text to OUTPUT_FILE. Returns elapsed seconds."""
    from piper import SynthesisConfig

    length_scale = 1.0 / SPEED   # piper uses length_scale (inverse of speed)

    syn_config = SynthesisConfig(
        volume=VOLUME,
        length_scale=length_scale,
        noise_scale=NOISE_SCALE,
        noise_w_scale=NOISE_W_SCALE,
        normalize_audio=NORMALIZE_AUDIO,
    )

    out_path = Path(OUTPUT_FILE)
    print(f"🔊 Synthesizing speech  →  {out_path}")
    print(f"   Speed: {SPEED}x  |  Volume: {VOLUME}  |  "
          f"Noise: {NOISE_SCALE}  |  Noise-W: {NOISE_W_SCALE}")
    print(f"   Text preview: {text[:80]}{'...' if len(text) > 80 else ''}\n")

    t0 = time.time()
    with wave.open(str(out_path), "wb") as wav_file:
        voice.synthesize_wav(text, wav_file, syn_config=syn_config)
    elapsed = time.time() - t0

    return elapsed


def main():
    print("\n" + "═" * 60)
    print("  🔊  Piper TTS — Text-to-Speech Generator")
    print("═" * 60 + "\n")

    start = time.time()

    # 1. Load text
    text = load_text()

    # 2. Load voice model
    voice = load_voice()

    # 3. Synthesize
    elapsed = synthesize(text, voice)

    # 4. Summary
    total = time.time() - start
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"✅ Done! WAV file saved to:  {Path(OUTPUT_FILE).resolve()}")
    print(f"   Synthesis time : {elapsed:.2f}s")
    print(f"   Total time     : {total:.2f}s")
    print(f"   Finished at    : {timestamp}\n")


if __name__ == "__main__":
    main()