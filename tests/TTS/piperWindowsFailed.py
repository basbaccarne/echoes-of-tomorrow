import subprocess
import time
from pathlib import Path
import sys

# Correcte paden
#PIPER_PATH = "/home/pi/i2s_audio_test/piper/"
PIPER_STEM = Path(r"C:/Users/fburger/piper/piper/")
PIPER_PATH = PIPER_STEM / "piper"
VOICE = PIPER_STEM / "voices/nl_NL-mls_5809-low.onnx"
TTS_OUTPUT = Path(r"C:/Users/fburger/OneDrive - UGent/Documents/Projects/echoes-of-tomorrow/tests/TTS/audio_out/")


def speak(text, outname, speed=1.0):
    """Text to speech - simpel"""
    print(f"🔊 Speaking (speed {speed}x): {text[:50]}...")
    t1 = time.time()
    
    # Paths
    OUTPUT_WAV = PIPER_STEM / outname
    VOICE_CONFIG = VOICE / ".json"
    #temp_text_file = PIPER_STEM / "temp.txt"

    cmd = [
        PIPER_PATH,
        "--model", VOICE,
        "--text", text,
        "--config", VOICE_CONFIG,
        "--output_file", outname,
        "--output_dir", TTS_OUTPUT
        #"--length_scale", str(speed)
    ]
    
    process = subprocess.run(
        cmd,
        #input=text.encode('utf-8'),
        capture_output=True
    )

    if process.returncode != 0:
        print("Error:", process.stderr.decode())
    else:
        print(f"Generated WAV at {output_wav}")

    t2 = time.time()
    print(f"⏱️  Generated in {t2-t1:.2f}s")

    return t2-t1


# Test
text = "Welkom bij de bibliotheek. Ik kan je helpen met informatie over toekomstbeelden."

print("\n1. Normale snelheid:")
speak(text, "speed1.wav", speed=1.0,)

print("\n2. Iets sneller:")
speak(text, "speed2.wav", speed=0.85)
# Test
text = "Welkom bij de bibliotheek. Ik kan je helpen met informatie over toekomstbeelden."

print("\n1. Normale snelheid:")
speak(text, "speed3.wav", speed=0.65)

print("\n2. Iets sneller:")
speak(text, "speed4.wav", speed=0.55)