# Echoes of Tomorrow
Echoes of Tomorrow is an installation developed for the [Comon](https://comon.gent/) expo at [De Krook](https://dekrook.be/).   
*Tinkered with* ❤ *by Bas Baccarne, Ben Robaeyst, ...*
 
## Project Description
Echoes of Tomorrow is an immersive, interactive installation that invites visitors to step into a dialogue with the future—literally. Grounded in the methodologies of Futures Research and speculative design, this experiential piece uses a powerful metaphorical and physical system to make possible futures tangible, audible, and emotionally resonant.   
At the heart of the installation stand three totemic structures, each representing a distinct future scenario. These futures are not predictions, but provocations—embodied visions of what could emerge based on the interplay of current social, environmental, and technological trends. Each totem channels a unique persona, brought to life through scripted AI-generated voice interactions, audio design, and environmental cues.


<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Echoes of Tomorrow](#echoes-of-tomorrow)
  - [Project Description](#project-description)
  - [Hack zone](#hack-zone)
    - [Capture microphone input (mic)](#capture-microphone-input-mic)
    - [Speech to text (STT)](#speech-to-text-stt)
    - [Integration layer](#integration-layer)
    - [Interpretation (LLM)](#interpretation-llm)
    - [Text to speech (TTS)](#text-to-speech-tts)
    - [Send audio (speaker)](#send-audio-speaker)
    - [General remarks](#general-remarks)
  - [Build zone](#build-zone)
    - [Key Components & Features:](#key-components--features)
    - [Set-up (3 seperate totems):](#set-up-3-seperate-totems)

<!-- /code_chunk_output -->



---

## Hack zone

* [General set-up](https://www.figma.com/board/wxgd1HG60FEPWjULjJxW3G/Untitled?node-id=0-1&t=mSymsbc2NLRJAKZq-1)

### Capture microphone input (mic)

**Hardware**
* ❌ Test: [Element 14 Wolfson Audio Card](/tests/mic/wolfson.md) (old raspis)
* ❌ Test: [Respeaker 2](/tests/mic/respeaker.md) (depricated old raspis)
* ❌ Test: USB microphone  (aborted, the other solutions are good enough and smaller)
* ✔️ Test: [Google Voice HAT](/tests/mic/voice_hat.md) (with button and speaker)
* ✍🏻 Test: [USB sound card](/tests/mic/usb%20_sound_card.md)
* 💬 Test: I²S microphone (e.g. INMP441)

**Software**
* ✔️ Test: [python audio capture](/tests/mic/python_record.py)

### Speech to text (STT)
* ✔️ Test: [faster-whisper](/tests/STT/readme.md)

### Integration layer
* ✍🏻 Test: [n8n](/tests/integration/readme.md)

### Interpretation (LLM)
* ✔️ Test: [Ollama](/tests/LLM/readme.md) - local but slowish
* ✔️ Test: [ChocoLlama](/tests/LLM/readme.md) - local, Flemish, bit realy slow
* ✔️ Test: [OpenAI API](/tests/LLM/readme.md) - quick, but cloud-based & maga-support
* 💬 Test: RAG system

### Text to speech (TTS)
* ✔️ test: [piper](/tests/TTS/readme.md)
* ✔️ test: [Hume AI](/tests/TTS/readme.md)
* ✔️ test: [Edge TTS](/tests/TTS/readme.md)

### Send audio (speaker)
* ❌ Test: Respeaker 2 (depricated old raspis)
* ❌ Test: USB speaker (aborted, the other solutions are good enough and smaller)   
* ✔️ Test: [USB sound card](/tests/speaker/usb_sound_card.md)
* ✔️ Test: [Google Voice HAT](/tests/speaker/voice_hat.md)
* 💬 Test: I²S DAC pre-amp (e.g. ADA3006)

### General remarks
**Latency challenge**
* Nvidia Jetson Orin Nano kan dit sneller maken (, maar duur > €500)
* Een lokale server kan dit sneller maken
* Een cloud serverice kan dit sneller maken

**Other things to think of**
* Dutch plosives (“p”, “t”, “k”) clip easily → lower mic gain
* Avoid long responses
* [Interesting read](https://medium.com/@martin.hodges/setting-up-a-mems-i2s-microphone-on-a-raspberry-pi-306248961043)   


---
## Build zone
1. Initialize Raspberry Pi & ```sudo apt update && sudo apt upgrade -y```
2. ...


---
### Key Components & Features:
🔮 The Totems of Time: Each totem is sculptural and symbolic, representing its future through material, color, and embedded media.   

e.g.:
* ```Utopia Totem```: Bioluminescent materials, soft glowing light, natural forms, harmonious soundscape.
* ```Dystopia Totem```: Harsh metals, fractured design, flickering lights, industrial droning ambient audio.
* ```Resilience Totem```: Reclaimed materials, adaptive design, warm lighting, layered textures of hope and struggle.

### Set-up (3 seperate totems):
(example)   

☎️ The Conversational Horns
Old-fashioned telephone receiver horns protrude from each totem. When lifted, they allow you to ask questions to the future.
Visitors can pose questions such as “What is work like in your world?” or “How do you care for the planet?”
Responses are generated through pre-written narratives powered by Futures Foresight techniques and character-driven voice AI, giving each persona a unique tone, worldview, and emotional cadence.

💬 The Personas
e.g.
Aurora (Utopia): A poet-ecologist from a post-scarcity society focused on harmony, sustainability, and collective wellbeing.
Rex (Dystopia): A weary scavenger-survivor in a fractured world dominated by surveillance, climate collapse, and scarcity.
Sol (Resilience): A community leader in a transitional, adaptive society where local systems, mutual aid, and innovation help people endure and thrive amid ongoing challenges.

🌐 Interactive Futures Table (optional)
A digital tabletop adjacent to the totems allows deeper engagement:
Visitors can explore data-driven scenarios, policy pathways, and personal stories associated with each future.

📜 The Futures Journal
As visitors exit, they are invited to contribute to a living archive of questions and reflections, either digitally or via physical postcards.

Echoes of Tomorrow turns abstract futures thinking into visceral, personal experience. By enabling direct dialogue with imagined future beings, the installation cultivates empathy, critical foresight, and agency. It asks visitors not only to listen—but to consider which future they want to help create.