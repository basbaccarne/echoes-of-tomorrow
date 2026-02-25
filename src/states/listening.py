import sounddevice as sd
import wavio
from gpiozero import Button
import time

button_stop = Button(3)
recording = []
fs = 44100
recording_active = False

def run():
    global recording, recording_active

    if not recording_active:
        print("Starting recording...")
        recording = []
        recording_active = True

    # record small chunk
    data = sd.rec(int(0.5 * fs), samplerate=fs, channels=1)
    sd.wait()
    recording.append(data)

    # stop on button 3 press
    if button_stop.is_pressed:
        print("Button 3 pressed → stopping recording")
        save()
        return "next_after_listen"  # your next state

    return None


def save():
    global recording, recording_active
    if recording:
        wavio.write("recorded.wav", np.concatenate(recording), fs, sampwidth=2)
        print("Recording saved")
    recording_active = False