# Dutch speech-to-text in Python
OpenAI's Whisper works well for Dutch and works great on Raspberry Pi.

**Installation**
```bash
pip install faster_whisper
```
* ```tiny```: ~1-2 seconden, redelijke nauwkeurigheid
* ```base```: ~2-3 seconden, goede nauwkeurigheid
* ```small```: ~3-5 seconden, beste nauwkeurigheid

**Latency challenge**
* Nvidia Jetson Orin Nano kan dit sneller maken (€500)
* Een lokale server kan dit sneller maken
* Een cloud serverice kan dit sneller maken

**Appearence fixes**
* Toevoegen van geluiden en animaties om de wachttijd te maskeren (sending your question to the future)