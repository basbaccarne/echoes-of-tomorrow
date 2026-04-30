from dotenv import load_dotenv
import os
import time
import wave
import subprocess
import platform
from elevenlabs.client import ElevenLabs
from elevenlabs.types import VoiceSettings

# Output path for the generated WAV file
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "output.wav")

# load variables from .env into environment
# Make sure to add ELEVENLABS_API_KEY=your_api_key_here to your .env file
load_dotenv()

# Check key
API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing ELEVENLABS_API_KEY in environment")

# Configure ElevenLabs client
client = ElevenLabs(
    api_key=API_KEY
)
print("ElevenLabs client configured")

# Generate speech from text
t_request = time.time()
print(f"[{t_request:.3f}] Sending TTS request...")
audio = client.text_to_speech.convert(
    text="De jeugd wordt dommer en dommer omdat de maatschappij sterk gericht is op prestaties en competentie, waardoor afwijkende denkwijzen en creativiteit niet worden gewaardeerd.\n\nEen voorbeeld is dat mijn zoon, Max, 12 jaar oud, elke dag op school bijna 6 uur op een digitaal leerplatform zit om zijn leerdoelen te halen, waardoor hij weinig tijd heeft om zijn eigen interesses te volgen. Het leerplatform, dat door de school wordt gekozen en wordt aangeboden door een groot platformbedrijf, geeft zijn prestaties continu door aan zijn ouders en leraren, waardoor hij voortdurend wordt gemotiveerd om beter te doen.",
    voice_id="Otc3wCRPKNSpn8EDImmM",  # free tier supports these voices https://elevenlabs.io/app/default-voices
    model_id="eleven_multilingual_v2",  # alt: eleven_multilingual_v2 / eleven_v3
    language_code="nl",
    voice_settings=VoiceSettings(
        stability=0.5,           # 0.0–1.0: lower = more expressive, higher = more monotone
        similarity_boost=0.75,   # 0.0–1.0: how closely to adhere to the original voice
        style=0.5,               # 0.0–1.0: style exaggeration (increases latency if > 0)
        use_speaker_boost=True,  # boosts similarity to original speaker (slightly higher latency)
        speed=1,                 # < 1.0 slows down, > 1.0 speeds up
    ),
    output_format="pcm_44100",   # raw 16-bit PCM at 44100 Hz, needed for WAV container
)

# Collect all audio bytes from the generator
t_stream_start = time.time()
print(f"[{t_stream_start:.3f}] Response received, streaming audio bytes... (+{t_stream_start - t_request:.2f}s)")
audio_bytes = b"".join(audio)
t_stream_done = time.time()
print(f"[{t_stream_done:.3f}] Audio stream complete — {len(audio_bytes):,} bytes (+{t_stream_done - t_stream_start:.2f}s)")

# Save as WAV file (PCM: 16-bit, mono, 44100 Hz)
with wave.open(OUTPUT_PATH, "wb") as wf:
    wf.setnchannels(1)   # mono
    wf.setsampwidth(2)   # 16-bit
    wf.setframerate(44100)
    wf.writeframes(audio_bytes)
t_saved = time.time()
print(f"[{t_saved:.3f}] WAV saved to {OUTPUT_PATH} (+{t_saved - t_stream_done:.2f}s)")

# Play from the saved WAV file — raw PCM bytes have no format header so play() can't decode them
print(f"[{t_saved:.3f}] Playing audio...")
sys_name = platform.system()
if sys_name == "Windows":
    subprocess.run(
        ["powershell", "-c", f"(New-Object Media.SoundPlayer '{OUTPUT_PATH}').PlaySync()"],
        check=True
    )
elif sys_name == "Darwin":
    subprocess.run(["afplay", OUTPUT_PATH], check=True)
else:
    subprocess.run(["aplay", OUTPUT_PATH], check=True)
t_done = time.time()
print(f"[{t_done:.3f}] Playback done — total elapsed: {t_done - t_request:.2f}s")
