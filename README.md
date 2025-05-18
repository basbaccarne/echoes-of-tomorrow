# Echoes of Tomorrow
Echoes of Tomorrow is an installation developed for the [Comon](https://comon.gent/) expo at [De Krook](https://dekrook.be/).   
*Tinkered with ❤ by Bas Baccarne, Ben Robaeyst, ...*
 
## Project Description:
Echoes of Tomorrow is an immersive, interactive installation that invites visitors to step into a dialogue with the future—literally. Grounded in the methodologies of Futures Research and speculative design, this experiential piece uses a powerful metaphorical and physical system to make possible futures tangible, audible, and emotionally resonant.   
At the heart of the installation stand three totemic structures, each representing a distinct future scenario. These futures are not predictions, but provocations—embodied visions of what could emerge based on the interplay of current social, environmental, and technological trends. Each totem channels a unique persona, brought to life through scripted AI-generated voice interactions, audio design, and environmental cues.

### Key Components & Features:
🔮 The Totems of Time
Each totem is sculptural and symbolic, representing its future through material, color, and embedded media:
e.g.:
* Utopia Totem: Bioluminescent materials, soft glowing light, natural forms, harmonious soundscape.
* Dystopia Totem: Harsh metals, fractured design, flickering lights, industrial droning ambient audio.
* Resilience Totem: Reclaimed materials, adaptive design, warm lighting, layered textures of hope and struggle.

### Set-up (3 seperate totems):
* Retro telephone horn
* Raspberry pi server
* Avatar

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

## Subchallenges
### Telephone interaction
Most retro style (landline, POTS [plain old telephone system]) telehone use a RJ11 connection to manage calling, voltages, audio, etc.     
In this case we have four options.
1. **USB telephone**. These are more expensive and do not always work with raspi.
2. Build our **own enclose** and embed speaker and microphone
3. Hack into the speaker lines and microphone lines by **tapping into tthe wires** that come directly from the peripherals
4. Use a **FXO (Foreign Exchange Office) modem** that works over the RJ11 line and manages power, signals, pick-up detection, ...    

Option 2 looks most interesting.   

* First experiments: [simple landline telehone](https://www.bol.com/be/nl/p/alcatel-t06-analoge-telefoon-zwart/9200000078556199/?bltgh=p3SP3cacIqewf-bT8EBMCg.4_14.15.ProductTitle) with the [Seeed Studio ReSpeaker 2 HAT](https://wiki.seeedstudio.com/ReSpeaker_2_Mics_Pi_HAT/)
* This is a rather hard path, instead: we'll work with the respeaker directly:
  recording:
  ```console
  python3 recording_examples/record.py 2>/dev/null
  ```
  play
  ```console
 aplay output.wav
  ```
