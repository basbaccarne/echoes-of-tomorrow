# The Grove DIP switch is a static switch meant to configure things

# Connection: power (3.3 or 5V), ground, sca, sdl (I²C)

# The module’s default I²C address is 0x03

# check if I²C is enabled on pi: sudo raspi-config 
    # > Interface Options → I2C → Enable (reboot if changed)
    
# to check if the device is detected: sudo i2cdetect -y 1
    # should show 0x03 in the table
    
# pip3 install smbus2

#!/usr/bin/env python3
import smbus2
import time

I2C_ADDR = 0x03  # default address
bus = smbus2.SMBus(1)  # I2C bus 1 on most Pis

def read_dip():
    try:
        # Some devices require a simple byte read:
        value = bus.read_byte(I2C_ADDR)
        # 'value' now has six bits (bit0..bit5) corresponding to switches
        return value
    except Exception as e:
        print("I2C read error:", e)
        return None

def print_state(val):
    if val is None:
        return
    states = []
    for i in range(6):
        # bit 0 = switch 1, bit 1 = switch 2, etc.
        state = 'ON' if (val & (1 << i)) == 0 else 'OFF'
        states.append(f"SW{i+1}:{state}")
    print(" ".join(states))

if __name__ == "__main__":
    while True:
        dip = read_dip()
        print_state(dip)
        time.sleep(1)
    