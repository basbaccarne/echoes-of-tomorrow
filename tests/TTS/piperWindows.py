import time
from pathlib import Path
import sys
import wave
from piper import PiperVoice, SynthesisConfig

TEXT_PATH = "./text_in/"
AUDIO_PATH = "./audio_out/"


voice = PiperVoice.load("./voices/nl_NL-mls_5809-low.onnx")

def speak(text, output_filename, speed=1.0):

    speed_inv = 1/speed
    OUTPUT_WAV = AUDIO_PATH + output_filename

    #print(f"🔊 Speaking (speed {speed_inv}x): {text[:50]}...")
    t1 = time.time()

    syn_config = SynthesisConfig(
        volume=0.5,  # half as loud
        length_scale=speed_inv,  # speed_inv times as slow
        noise_scale=1.0,  # more audio variation
        noise_w_scale=1.0,  # more speaking variation
        normalize_audio=False, # use raw audio from voice
    )

    with open(text, 'r') as file:
        txtinput = file.read().replace('\n', '')

    with wave.open(OUTPUT_WAV, "wb") as wav_file:
        voice.synthesize_wav(txtinput, wav_file, syn_config= syn_config)

    t2 = time.time()
    print(f"⏱️  Generated in {t2-t1:.2f}s")

    return t2-t1


#Test
print("\n1. Normale snelheid:")
#INPUT_TXT = "Welkom bij de bibliotheek. Ik kan je helpen met informatie over toekomstbeelden."
INPUT_TXT = TEXT_PATH + "test.txt"
speak(INPUT_TXT, "test.wav")


