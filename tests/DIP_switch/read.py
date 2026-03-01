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

# Single careful read with recovery time between attempts
for i in range(5):
    try:
        result = bus.read_byte(ADDR)
        print(f"read {i}: 0x{result:02X} = {result:08b}")
    except OSError as e:
        print(f"read {i}: ERROR - {e}")
    time.sleep(1)  # give the chip a full second to recover