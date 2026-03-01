# The Grove DIP switch is a static switch meant to configure thing
# Connection: power (3.3 or 5V), ground, sca, sdl (I²C)
# The module’s default I²C address is 0x03

# check if I²C is enabled on pi: sudo raspi-config 
    # > Interface Options → I2C → Enable (reboot if changed)

# install grove libraries: sudo pip3 install grove.py (you'll need pip)

from grove.factory import Factory
from grove.button import Button
import time

# create the multi switch (I2C device index 0)
switch = Factory.getButton("I2C", 0)

def on_event(index, event, tm):
    # only react when level changes (ON/OFF)
    if event & Button.EV_LEVEL_CHANGED:
        print_dip_state()

def print_dip_state():
    bits = 0
    states = []

    # read 6 switches
    for i in range(6):
        # RAW_STATUS == HIGH means OFF in DIP logic
        if switch.btn.status(i) == Button.EV_RAW_STATUS:
            states.append(f"SW{i+1}:ON")
            bits |= (1 << i)
        else:
            states.append(f"SW{i+1}:OFF")

    print(" ".join(states), "-> value:", bits)

# attach event handler
switch.on_event(on_event)

print("🎛️ DIP test running — toggle switches now")
print("Ctrl+C to stop\n")

# initial read
print_dip_state()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nstopped")