# The Grove DIP switch is a static switch meant to configure thing
# Connection: power (3.3 or 5V), ground, sca, sdl (I²C)
# The module’s default I²C address is 0x03

# check if I²C is enabled on pi: sudo raspi-config 
    # > Interface Options → I2C → Enable (reboot if changed)

# you should see the device at address 0x03 using sudo i2cdetect -y -a 1

import smbus2

bus = smbus2.SMBus(1)
ADDR = 0x03

# Read raw bytes from several registers so we can see what's what
for reg in range(0x00, 0x08):
    try:
        data = bus.read_i2c_block_data(ADDR, reg, 4)
        print(f"reg 0x{reg:02X}: {[hex(b) for b in data]}")
    except OSError as e:
        print(f"reg 0x{reg:02X}: ERROR - {e}")