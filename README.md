# Echoes of Tomorrow
Echoes of Tomorrow is an installation developed for the [Comon](https://comon.gent/) expo at [De Krook](https://dekrook.be/).   
*Tinkered with* ❤ *by Bas Baccarne, Ben Robaeyst, Tim Theys, Fran Burger, Julien Verplanken, Yannick Christiaens, Jeroen Bourgonjon, Wanda Gaertner, Stephanie Van Hove, Azra Verlee, Axel Kiekens, Morgane Spanhove & Flo Van Hove*.
 
## Project Description
Echoes of Tomorrow is an immersive, interactive installation that invites visitors to step into a dialogue with the future—literally. Grounded in the methodologies of Futures Research and speculative design, this experiential piece uses a powerful metaphorical and physical system to make possible futures tangible, audible, and emotionally resonant. At the heart of the installation stand four telephone boots, each representing a distinct future scenario. These futures are not predictions, but provocations—embodied visions of what could emerge based on the interplay of current social, environmental, and technological trends. Each totem channels a unique persona, brought to life through scripted AI-generated voice interactions, audio design, and environmental cues.

---

# Hack zone

* [General set-up](https://www.figma.com/board/wxgd1HG60FEPWjULjJxW3G/Untitled?node-id=0-1&t=mSymsbc2NLRJAKZq-1)

# Bill of materials
| part  | count  | price per part| source |
|---|---|---| ---|
| [Raspberry pi4 4GB](https://www.kiwi-electronics.com/nl/raspberry-pi-4-model-b-4gb-4268) |  4 | €80 | ✔ kiwi |
| [Voeding raspi 27w usb-c](https://www.kiwi-electronics.com/nl/raspberry-pi-27w-usb-c-power-supply-zwart-eu-11582) | 4 | €13 | ✔ kiwi |
| [Microswitch](https://www.kiwi-electronics.com/nl/mini-microschakelaar-spdt-offset-lever-2-pack-2499)| 4 | €3 | ✔ kiwi |
| [Grove 6-position DIP switch](https://www.kiwi-electronics.com/nl/grove-6-position-dip-switch-20587?search=grove%206-position%20DIP%20switch) |4 | €5,43| ✔ kiwi |
| [Led ring](https://www.kiwi-electronics.com/nl/grove-rgb-led-ring-16-ws2813-mini-10313)| 4 | €13 | ✔ kiwi |
| SD kaartje 32gb (snel) | 4 | €10 | gotron |
| Router | 1 | €60 | ✔ gotron | 
| USB WiFi dongle server | 1 | €10 | ✔ grotron |
| Flat arcade button | 4 | €1,5 | IDE lab |
| Server | 1 | -- | ✔ desktop IDE lab|
| 3.5mm jack telephone horn | 4 | -- | IDE lab + webshop tbd |
| 3.5 mm jack to usb dongle|4| €9 | ✔ amazon |
| [or] USB telephone horn |4| €20 | webshop tbd |


# 3D model
* [Fusion link](https://a360.co/4aQVtJP)

---
# Build zone pi
**wiring**
* Connect **DIP switch** to ```3.3V```(red), ```ground```(black), ```SDA/GPIO2```(white), and ```SCL/GPIO3```(yellow)
* Connect **LED ring** to ```5V``` (red) ```ground``` (black) and ```GPIO4``` (yellow)
* Connect **horn button** to ``GPIO17`` and ``GROUND``
* Connect **hashtag button** to ``GPIO27`` and ``GROUND``

* Connect **USB telephone** to ```USB```
* Attach power
* Configure SD card (pi OS lite is fine)
<div align="left">  
 <img src="/img/pinout.png" width="600"> 
</div>

**software**
1. Initialize Raspberry Pi & ```sudo apt update && sudo apt upgrade -y```
2. Software Installations - ```sudo apt install git i2c-tools python3-pip -y```
3. Get the main repo - ```git clone https://github.com/basbaccarne/echoes-of-tomorrow```
4. Install python libraries - ```pip install pyyaml requests```
5. Enable I²C in raspi-config
6. Set ID
7. Set service
8. Switch to offline network comon


# Build zone server
1. On a fresh Ubuntu server: ```sudo apt update && sudo apt upgrade -y```
2. Software Installations - ```sudo apt install git nodejs npm -y```
3. Get the main repo - ```git clone https://github.com/basbaccarne/echoes-of-tomorrow```
4. Install n8n
5. Install ollama


# State machine (pi & server)

```mermaid
flowchart TB
    classDef pi     fill:#BCCCE0,stroke-width:0
    classDef server fill:#BF98A0,stroke-width:0

    subgraph Pi ["Raspberry Pi"]
        direction TB
        IDLE:::pi-->|horn release| PLAY_WELCOME:::pi
        PLAY_WELCOME     -->|audio done| RECORDING:::pi
        RECORDING        -->|# press| SENDING:::pi
        SENDING          --> WAITING:::pi
        WAITING          -->|file detected| RESPONDING:::pi
        RESPONDING:::pi  -->|audio done| IDLE
    end

    subgraph Srv ["Server"]
        direction TB
        RECEIVE:::server -->|http complete| STT:::server
        STT              -->|transcribed| N8N:::server
        N8N              -->|response| TTS:::server
        TTS              -->|wav ready| SEND_BACK:::server
        SEND_BACK        --> RECEIVE
    end

    SENDING   -->|upload| RECEIVE
    SEND_BACK -->|deliver| WAITING

```

# File structure on the server
```
/home/
  /io/
    echoes-of-tomorrow/
        audio_files/
            question_0.wav
            question_0.txt
            reponse_0.txt
            response_0.wav

            question_1.wav
            question_1.txt
            reponse_1.txt
            response_1.wav

            question_2.wav
            question_2.txt
            reponse_2.txt
            response_2.wav

            question_3.wav
            question_3.txt
            reponse_3.txt
            response_3.wav
```

# Tests
## Capture microphone input (mic)

**Hardware**
* ❌ Test: [Element 14 Wolfson Audio Card](/tests/mic/wolfson.md) (old raspis)
* ❌ Test: [Respeaker 2](/tests/mic/respeaker.md) (depricated old raspis)
* ❌ Test: USB microphone  (aborted, the other solutions are good enough and smaller)
* ✔️ Test: [Google Voice HAT](/tests/mic/voice_hat.md) (with button and speaker)
* ✔️ Test: [USB sound card](/tests/mic/usb%20_sound_card.md)
* ✔️ Test: [I²S microphone](/tests/mic/I2S.md) (e.g. INMP441)

**Software**
* ✔️ Test: [python audio capture](/tests/mic/python_record.py)

## Speech to text (STT)
* ✔️ Test: [faster-whisper](/tests/STT/readme.md)

## Integration layer
* ✍🏻 Test: [n8n](/tests/integration/readme.md)

## Interpretation (LLM)
* ✔️ Test: [Ollama](/tests/LLM/readme.md) - local but slowish
* ✔️ Test: [ChocoLlama](/tests/LLM/readme.md) - local, Flemish, bit realy slow
* ✔️ Test: [OpenAI API](/tests/LLM/readme.md) - quick, but cloud-based & maga-support
* 💬 Test: RAG system

## Text to speech (TTS)
* ✔️ test: [piper](/tests/TTS/readme.md)
* ✔️ test: [Hume AI](/tests/TTS/readme.md)
* ✔️ test: [Edge TTS](/tests/TTS/readme.md)

## Send audio (speaker)
* ❌ Test: Respeaker 2 (depricated old raspis)
* ❌ Test: USB speaker (aborted, the other solutions are good enough and smaller)   
* ✔️ Test: [USB sound card](/tests/speaker/usb_sound_card.md)
* ✔️ Test: [Google Voice HAT](/tests/speaker/voice_hat.md)
* ✔️ Test: [I²S DAC pre-amp](/tests/speaker/I2S.md) (e.g. ADA3006)

## General remarks
**Latency challenge**
* Nvidia Jetson Orin Nano kan dit sneller maken (, maar duur > €500)
* Een lokale server kan dit sneller maken
* Een cloud serverice kan dit sneller maken

**Other things to think of**
* Dutch plosives (“p”, “t”, “k”) clip easily → lower mic gain
* Avoid long responses
* [Interesting read](https://medium.com/@martin.hodges/setting-up-a-mems-i2s-microphone-on-a-raspberry-pi-306248961043)   