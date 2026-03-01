# The Grove DIP switch is a static switch meant to configure thing
# Connection: power (3.3 or 5V), ground, sca, sdl (I²C)
# The module’s default I²C address is 0x03

# check if I²C is enabled on pi: sudo raspi-config 
    # > Interface Options → I2C → Enable (reboot if changed)

# you should see the device at address 0x03 using sudo i2cdetect -y -a 1

import smbus2

bus = smbus2.SMBus(1)
ADDR = 0x03

# No register — just read a raw byte directly
for _ in range(10):
    try:
        result = bus.read_byte(ADDR)
        print(f"raw byte: 0x{result:02X} = {result:08b}")
    except OSError as e:
        print(f"ERROR: {e}")