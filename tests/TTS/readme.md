# Text to speech with piper
```bash
# Download
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz
# Unzip
tar -xzf piper_arm64.tar.gz
cd piper
# Add voices
mkdir -p voices

# Download nl_NL-mls_5809-low (snel, goede kwaliteit)
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx -P voices/
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx.json -P voices/

# Download nl_NL-mls-medium (betere kwaliteit, iets langzamer)
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/nl/nl_NL/mls/medium/nl_NL-mls-medium.onnx -P voices/
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/nl/nl_NL/mls/medium/nl_NL-mls-medium.onnx.json -P voices/
```

test
```bash
echo "Hallo, dit is een test van de Nederlandse stem synthese." | ./piper --model voices/nl_NL-mls_5809-low.onnx --output_file test.wav
```

[testcode](/tests/TTS/piper.py)

# Text to speech with hume AI
No Dutch support (yet?)
```bash
pip install hume
```

[testcode](/tests/TTS/hume_test.py)

# Text to speech with edge TTS
```bash
# install
pip install TTS
# Get list of voices
edge-tts --list-voices | grep nl
# run scipt
python3 edgetts_test.py
# play outcome
ffplay tts_output.mp3
```
[testcode](/tests/TTS/edgetts_test.py)