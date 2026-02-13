from faster_whisper import WhisperModel
import warnings
import os
import time

# Onderdruk alle warnings
warnings.filterwarnings("ignore")
os.environ["OMP_NUM_THREADS"] = "4"

print("Loading faster-whisper model...")
load_start = time.time()
model = WhisperModel(
    "small", 
    device="cpu",
    compute_type="int8"
)
load_time = time.time() - load_start
print(f"✓ Model loaded in {load_time:.2f} seconds!")

def transcribe_file(filename):
    """Transcribe with faster-whisper"""
    print(f"Transcribing '{filename}'...")
    
    transcribe_start = time.time()
    
    segments, info = model.transcribe(
        filename,
        language="nl",
        beam_size=1,
        vad_filter=False,
        without_timestamps=True
    )
    
    print("Processing segments...")
    segments_list = list(segments)
    
    transcribe_time = time.time() - transcribe_start
    
    print(f"Found {len(segments_list)} segments")
    print(f"⏱️  Transcription took {transcribe_time:.2f} seconds")
    
    text = " ".join([segment.text for segment in segments_list])
    
    print("✓ Transcription complete!")
    return text

# Use it
print("="*50)
total_start = time.time()
text = transcribe_file("test.wav")
total_time = time.time() - total_start
print("="*50)
print(f"Transcribed text:\n'{text}'")
print("="*50)
print(f"⏱️  Total time: {total_time:.2f} seconds")
print("="*50)