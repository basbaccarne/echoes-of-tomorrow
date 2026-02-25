from gpiozero import Button
import time

button_horn = Button(4)
debounce = 0.3

def run():
    # wait for release event
    if button_horn.is_pressed:
        while button_horn.is_pressed:
            time.sleep(0.01)

        print("Button 4 released → switching state")
        time.sleep(debounce)

        return "nextstate"   # <-- name of next state module (states/nextstate.py)

    return None