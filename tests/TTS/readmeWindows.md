# Text to speech with piper
```bash
# While server has internet access, install piper with pip
python3 -m pip install piper
# Install voices
python3 -m piper.download_voices ./voices/nl_NL-mls_5809-low

# Read in text file from folder text_in and write wav output file into folder audio_out
[testcode](/tests/TTS/piperWindows.py)
```

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