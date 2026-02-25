import sounddevice as sd
import numpy as np
import wavio
from hardware import button_stop

fs = 44100
recording = []

def run():
    global recording

    print("Recording chunk...")

    data = sd.rec(int(0.5 * fs), samplerate=fs, channels=1)
    sd.wait()
    recording.append(data)

    if button_stop.is_pressed:
        print("Button 3 pressed → stop recording")
        save()
        return "idle"

    return None


def save():
    if recording:
        audio = np.concatenate(recording)
        wavio.write("recorded.wav", audio, fs, sampwidth=2)
        print("Recording saved")