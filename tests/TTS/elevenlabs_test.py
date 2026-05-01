from dotenv import load_dotenv
import os
import time
import wave
from elevenlabs.client import ElevenLabs
from elevenlabs.types import VoiceSettings

load_dotenv()

DEFAULT_VOICE_ID = "Otc3wCRPKNSpn8EDImmM"  # https://elevenlabs.io/app/default-voices
DEFAULT_MODEL_ID = "eleven_multilingual_v2"
DEFAULT_OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.wav")


def text_to_speech(
    text: str,
    output_path: str = DEFAULT_OUTPUT_PATH,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = DEFAULT_MODEL_ID,
    language_code: str = "nl",
) -> str:
    """Convert text to speech and save as WAV. Returns output_path."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("Missing ELEVENLABS_API_KEY in environment")

    client = ElevenLabs(api_key=api_key)

    t_start = time.time()
    print(f"[TTS] Sending request...")
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        language_code=language_code,
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.5,
            use_speaker_boost=True,
            speed=1,
        ),
        output_format="pcm_44100",  # raw 16-bit mono PCM at 44100 Hz, needed for WAV container
    )

    t_received = time.time()
    print(f"[TTS] Response received ({t_received - t_start:.2f}s), collecting bytes...")
    audio_bytes = audio if isinstance(audio, bytes) else b"".join(audio)
    t_collected = time.time()
    print(f"[TTS] {len(audio_bytes):,} bytes collected ({t_collected - t_received:.2f}s)")

    with wave.open(output_path, "wb") as wf:
        wf.setnchannels(1)   # mono
        wf.setsampwidth(2)   # 16-bit
        wf.setframerate(44100)
        wf.writeframes(audio_bytes)
    t_saved = time.time()
    print(f"[TTS] Saved to {output_path} ({t_saved - t_collected:.2f}s) | total: {t_saved - t_start:.2f}s")

    return output_path


if __name__ == "__main__":
    TEXT = (
        "De jeugd wordt dommer en dommer omdat de maatschappij sterk gericht is op prestaties en competentie, "
        "waardoor afwijkende denkwijzen en creativiteit niet worden gewaardeerd.\n\n"
        "Een voorbeeld is dat mijn zoon, Max, 12 jaar oud, elke dag op school bijna 6 uur op een digitaal "
        "leerplatform zit om zijn leerdoelen te halen, waardoor hij weinig tijd heeft om zijn eigen interesses "
        "te volgen. Het leerplatform, dat door de school wordt gekozen en wordt aangeboden door een groot "
        "platformbedrijf, geeft zijn prestaties continu door aan zijn ouders en leraren, waardoor hij "
        "voortdurend wordt gemotiveerd om beter te doen."
    )
    path = text_to_speech(TEXT)
    print(f"WAV file: {path}")
