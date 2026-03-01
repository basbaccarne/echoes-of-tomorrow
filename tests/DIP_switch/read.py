# The Grove DIP switch is a static switch meant to configure thing
# Connection: power (3.3 or 5V), ground, sda, scl (I²C)
# The module’s default I²C address is 0x03
# But without the grove hat for raspi this is a bit of a head ache
# Reading stable i²C data requuires a connection of both SCL and SDA to 3.3V trhough a 4.7k restistor
# The grove hat has these pullups built in, but if you are using a breadboard you will need to add them yourself 

# check if I²C is enabled on pi: sudo raspi-config 
    # > Interface Options → I2C → Enable (reboot if changed)

# you should see the device at address 0x03 using sudo i2cdetect -y -a 1

import smbus2
import time

bus = smbus2.SMBus(1)
ADDR = 0x03

# The chip sends a 10-byte packet:
# bytes 0-3: event header (uint32)
# bytes 4-9: one byte per switch (6 switches)
# For each switch byte: bit 0 = raw status (0=ON, 1=OFF)

import smbus2, time

bus = smbus2.SMBus(1)
ADDR = 0x03

while True:
    try:
        msg = smbus2.i2c_msg.read(ADDR, 10)
        bus.i2c_rdwr(msg)
        data = list(msg)
        print("─" * 30)
        for i in range(6):
            state = "ON " if not (data[4+i] & 0x01) else "OFF"
            print(f"  Switch {i+1}: {state}")
    except OSError as e:
        print(f"ERROR: {e}")
    time.sleep(0.5)