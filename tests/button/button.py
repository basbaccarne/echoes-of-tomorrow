from gpiozero import Button
import time

# Connect button_horn to GPIO17 and GROUND
# Connect button_hashtag  to GPIO27 and GROUND


button_horn = Button(17)
button_hashtag = Button(27)

debounce = 0.3

while True:
    # --- Pin 4: trigger on RELEASE ---
    if button_horn.is_pressed:
        while button_horn.is_pressed:
            time.sleep(0.01)

        print("Pin 4 released - phone picked up")
        time.sleep(debounce)

    # --- Pin 3: trigger on PRESS ---
    if button_hashtag.is_pressed:
        print("Pin 3 pressed")

        # wait until released to avoid repeat triggers
        while button_hashtag.is_pressed:
            time.sleep(0.01)

        time.sleep(debounce)