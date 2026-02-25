from hardware import button_horn
import time

debounce = 0.3

def run():
    if button_horn.is_pressed:
        while button_horn.is_pressed:
            time.sleep(0.01)

        print("Button 4 released → play welcome")
        time.sleep(debounce)
        return "play_welcome"

    return None