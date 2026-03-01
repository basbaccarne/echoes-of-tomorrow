# The Grove DIP switch is a static switch meant to configure thing
# Connection: power (3.3 or 5V), ground, sca, sdl (I²C)
# The module’s default I²C address is 0x03

# check if I²C is enabled on pi: sudo raspi-config 
    # > Interface Options → I2C → Enable (reboot if changed)

# you should see the device at address 0x03 using sudo i2cdetect -y -a 1


import smbus2
import time

bus = smbus2.SMBus(1)
ADDR = 0x03
REG_INPUT = 0x01

def read_switches():
    try:
        data = bus.read_i2c_block_data(ADDR, REG_INPUT, 2)
        return data[0]
    except OSError as e:
        print(f"I2C error: {e}")
        return None

last = None
while True:
    val = read_switches()
    if val is not None and val != last:
        last = val
        print("─" * 30)
        for i in range(6):
            # Bit LOW (0) = switch ON, bit HIGH (1) = switch OFF
            state = "ON " if not (val & (1 << i)) else "OFF"
            print(f"  Switch {i+1}: {state}")
    time.sleep(0.1)