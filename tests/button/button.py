from gpiozero import Button
button_horn = Button(4)
debounce = 0.3
if button_horn.is_pressed:
            # Wacht op release
            while button_horn.is_pressed:
                time.sleep(0.01)
            print("Button released - phone picked up")
            time.sleep(debounce)