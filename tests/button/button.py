from gpiozero import Button
import time

button_horn = Button(4)
debounce = 0.3

while True:
    if button_horn.is_pressed:
        # Wait for release
        while button_horn.is_pressed:
            time.sleep(0.01)

        print("Button released - phone picked up")
        time.sleep(debounce)