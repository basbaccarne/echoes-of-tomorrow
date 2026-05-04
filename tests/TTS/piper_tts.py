import time
import wave
from pathlib import Path

DEFAULT_OUTPUT_PATH = str(Path(__file__).parent / "output_piper.wav")
DEFAULT_VOICE_PATH = "/home/io/echoes-of-tomorrow/src_server/voices/nl_BE-rdh-medium.onnx"


def text_to_speech(text: str, output_path: str, voice, speed: float = 0.8) -> str:
    """Synthesize text using a preloaded Piper voice. Returns output_path."""
    from piper import SynthesisConfig

    t_start = time.time()
    print(f"[Piper] Synthesizing...")

    syn_config = SynthesisConfig(
        volume=1,
        length_scale=1 / speed,
        noise_scale=0.8,
        noise_w_scale=1.0,
        normalize_audio=False,
    )

    with wave.open(output_path, "wb") as wav_file:
        voice.synthesize_wav(text, wav_file, syn_config=syn_config)

    elapsed = time.time() - t_start
    print(f"[Piper] Done in {elapsed:.2f}s → {output_path}")

    return output_path


if __name__ == "__main__":
    from piper import PiperVoice

    TEXT = "Hallo, dit is een test van de Piper tekst-naar-spraak engine."
    print(f"[Piper] Loading voice from {DEFAULT_VOICE_PATH}...")
    v = PiperVoice.load(DEFAULT_VOICE_PATH)
    path = text_to_speech(TEXT, DEFAULT_OUTPUT_PATH, v)
    print(f"WAV file: {path}")
