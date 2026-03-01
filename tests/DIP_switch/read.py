# The Grove DIP switch is a static switch meant to configure thing
# Connection: power (3.3 or 5V), ground, sca, sdl (I²C)
# The module’s default I²C address is 0x03

# check if I²C is enabled on pi: sudo raspi-config 
    # > Interface Options → I2C → Enable (reboot if changed)

# install grove libraries: sudo pip3 install grove.py (you'll need pip)

import smbus2
import time

bus = smbus2.SMBus(1)
ADDR = 0x03

# The device returns 2 bytes; byte 0 is the switch bitmask
# Bit = 0 means ON (pulled low), 1 means OFF

while True:
    try:
        data = bus.read_i2c_block_data(ADDR, 0, 2)
        switches = data[0]
        print("─" * 30)
        for i in range(6):
            state = "ON " if not (switches & (1 << i)) else "OFF"
            print(f"  Switch {i+1}: {state}")
        time.sleep(0.5)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)