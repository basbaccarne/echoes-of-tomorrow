import subprocess
import time

# Correcte paden
PIPER_PATH = "/home/pi/i2s_audio_test/piper/piper"  # Let op: /piper/piper
VOICE = "/home/pi/i2s_audio_test/piper/voices/nl_NL-mls_5809-low.onnx"

def speak(text, speed=1.0):
    """Text to speech - simpel"""
    print(f"🔊 Speaking (speed {speed}x): {text[:50]}...")
    
    t1 = time.time()
    
    cmd = [
        PIPER_PATH,
        "--model", VOICE,
        "--output_file", "temp.wav",
        "--length_scale", str(speed)
    ]
    
    process = subprocess.run(
        cmd,
        input=text.encode('utf-8'),
        capture_output=True
    )
    
    t2 = time.time()
    print(f"⏱️  Generated in {t2-t1:.2f}s")
    
    # Speel af
    subprocess.run(["aplay", "temp.wav"], 
                   stdout=subprocess.DEVNULL, 
                   stderr=subprocess.DEVNULL)
    
    return t2-t1

# Test
text = "Welkom bij de bibliotheek. Ik kan je helpen met informatie over toekomstbeelden."

print("\n1. Normale snelheid:")
speak(text, speed=1.0)

print("\n2. Iets sneller:")
speak(text, speed=0.85)