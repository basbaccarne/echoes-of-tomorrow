# Capture audio using the Google AIY voice hat
Hardware: [AIY Voice Kit](https://aiyprojects.withgoogle.com/voice/)
Pinout: [schematic](https://github.com/google/aiyprojects-raspbian/blob/aiyprojects/schematics/voice_hat/voice_hat.pdf)

* Get the latest release of the image from the [Github repo](https://github.com/google/aiyprojects-raspbian/releases) and burn it on an SD card
* Or add the AIY software to an [existing raspi OS](https://github.com/google/aiyprojects-raspbian/blob/aiyprojects/HACKING.md#install-aiy-software-on-an-existing-raspbian-system)
* Or work with the bare components

**Add the I2S mic** 
```bash
sudo nano /boot/config.txt
```
```ini
dtoverlay=googlevoicehat-soundcard
```
```bash
sudo reboot
```
**Test it**
```bash
arecord -l
arecord -D plughw:2,0 -f cd -d 2 test.wav
aplay test.wav
```
* ```-D``` specifies the audio device to record from.
* ```plughw```: converts the mono 32-bit I²S mic signal to standard WAV automatically
* ```2,0```: [ALSA card number for the I²S microphone], [sub-device on that card]
* ```-f cd```: record in standard 16-bit 44.1 kHz stereo (CD-quality)
* ```-d 2```: stop after 2 seconds
* ```test.wav```: save the recording as test.wav


**Set the speaker**
Check if the speaker it detected
```bash
aplay -l 
alsamixer
```
Test the speaker
```bash
aplay /usr/share/sounds/alsa/Front_Center.wav
aplay /usr/share/sounds/alsa/Rear_Left.wav
```

**Test the button**
Install GPIO lib for python
```bash
sudo apt install python3-gpiozero
```

Wiring on the old HAT
|  color    | function | connected to |
|:---|:---|:---|
| Black |Button common	| GND |
| White	| Button NO (normally open) | GPIO 23 |
| Red	| LED anode	| GPIO 25 (5V through resistor) |
| Blue	| LED cathode | GND |

Create a Python script to test
```python
from gpiozero import Button
from signal import pause

# v1 kit: white wire → GPIO23
button = Button(23)

button.when_pressed = lambda: print("Button pressed!")
button.when_released = lambda: print("Button released!")

pause()
```
