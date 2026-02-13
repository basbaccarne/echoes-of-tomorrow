import sounddevice as sd
import soundfile as sf
import numpy as np

# --- Configuration ---
duration = 10
samplerate = 16000
channels = 1
filename = "test.wav"
gain = 5.0  # Volume versterking (pas aan naar wens)

# --- Record audio ---
print(f"Recording {duration} seconds...")
recording = sd.rec(
    int(duration * samplerate), 
    samplerate=samplerate, 
    channels=channels, 
    dtype='float32'  # float32 voor gain processing
)
sd.wait()

print("Processing audio...")
# Verhoog volume
amplified = recording * gain

# Voorkom clipping
amplified = np.clip(amplified, -1.0, 1.0)

# --- Save to WAV file ---
sf.write(filename, amplified, samplerate)
print(f"✓ Saved amplified recording to {filename}")