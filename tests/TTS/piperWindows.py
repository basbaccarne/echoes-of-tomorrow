import wave
from piper import PiperVoice, SynthesisConfig

TEXT_PATH = "./text_in/test.txt"  

syn_config = SynthesisConfig(
    volume=0.5,  # half as loud
    length_scale=2.0,  # twice as slow
    noise_scale=1.0,  # more audio variation
    noise_w_scale=1.0,  # more speaking variation
    normalize_audio=False, # use raw audio from voice
)

voice = PiperVoice.load("./voices/nl_NL-mls_5809-low.onnx")
with wave.open("./audio_out/test.wav", "wb") as wav_file:
    voice.synthesize_wav("Welkom in de Krook! Wat leuk dat je de weg naar ons hebt gevonden!", wav_file)

#