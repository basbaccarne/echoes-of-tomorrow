from dotenv import load_dotenv
import os
from elevenlabs.client import ElevenLabs
from elevenlabs.types import VoiceSettings
from elevenlabs.play import play

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
print("✅ ElevenLabs client configured successfully")

# Generate speech from text
print(f"🔊 Generating audio from text...")
audio = client.text_to_speech.convert(    
    text="De jeugd wordt dommer en dommer omdat de maatschappij sterk gericht is op prestaties en competentie, waardoor afwijkende denkwijzen en creativiteit niet worden gewaardeerd.\n\nEen voorbeeld is dat mijn zoon, Max, 12 jaar oud, elke dag op school bijna 6 uur op een digitaal leerplatform zit om zijn leerdoelen te halen, waardoor hij weinig tijd heeft om zijn eigen interesses te volgen. Het leerplatform, dat door de school wordt gekozen en wordt aangeboden door een groot platformbedrijf, geeft zijn prestaties continu door aan zijn ouders en leraren, waardoor hij voortdurend wordt gemotiveerd om beter te doen.",
    voice_id="IKne3meq5aSn9XLyUdCD", # free tier supports these voices https://elevenlabs.io/app/default-voices
    model_id="eleven_v3", # alt:  eleven_multilingual_v2,
    language_code="nl",
    voice_settings=VoiceSettings(
        stability=0.5,           # 0.0–1.0: lower = more expressive, higher = more monotone
        similarity_boost=0.75,   # 0.0–1.0: how closely to adhere to the original voice
        style=0.5,               # 0.0–1.0: style exaggeration (increases latency if > 0)
        use_speaker_boost=True,  # boosts similarity to original speaker (slightly higher latency)
        speed=1,               # < 1.0 slows down, > 1.0 speeds up
    ),
    output_format="mp3_44100_128",
)

# Play the generated audio
play(audio)