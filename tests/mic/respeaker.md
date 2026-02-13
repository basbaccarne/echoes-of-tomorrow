# Capture audio using a ReSpeaker 2 HAT
Hardware: [ReSpeaker 2-Mics Pi HAT](https://wiki.seeedstudio.com/ReSpeaker_2_Mics_Pi_HAT/)
📒[Full documentation](https://wiki.seeedstudio.com/ReSpeaker_2_Mics_Pi_HAT_Raspberry/)

**Specs**
* **Input**: This HAT has two built in mics (stereo) & is designed for AI and voice applications.
* **Output**: 3.5mm Audio Jack or JST 2.0 Speaker (⚠️ provide extra power when using the speaker modules)
* **Extra**: It also includes 3 APA102 **RGB LEDs** (SPI), 1 User **Button** (GPIO17) and 2 on-board **Grove interfaces** (2C-1 & GPIO12 | GPIO13)

**Driver**
You'll need the [seeed-voicecard driver](https://github.com/respeaker/seeed-voicecard) first.
The documentation suggests a **32-bit OS** version (check this with ```uname -m``` - this should be armv71).
The recommended OS is Raspberry Pi OS 32-bit [Bullseye](https://www.raspberrypi.com/software/operating-systems/).
⚠️Getting this to work on a raspi 5 is a pain in the ass.
```bash
sudo apt install linux-headers-$(uname -r)
git clone https://github.com/respeaker/seeed-voicecard
cd seeed-voicecard
sudo ./install.sh
sudo reboot
```
Check if things are recognized
```bash
arecord -l   # list capture (input) devices
aplay -l     # list playback (output) devices
```