from hardware import button_horn
import time

debounce = 0.3

def run():
    # after release 
    if button_horn.is_pressed:
        while button_horn.is_pressed:
            time.sleep(0.01)
            
        # go to the next state (play welcome)
        print("\n📞   The horn has been picked up")
        time.sleep(debounce)
        return "play_welcome"

    return None