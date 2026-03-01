# The Grove DIP switch is a static switch meant to configure thing
# Connection: power (3.3 or 5V), ground, sda, scl (I²C)
# The module’s default I²C address is 0x03
# But without the grove hat for raspi this is a bit of a head ache
# Reading stable i²C data requuires a connection of both SCL and SDA to 3.3V trhough a 4.7k restistor
# The grove hat has these pullups built in, but if you are using a breadboard you will need to add them yourself 

# extra insight (might render the above obsolete):
# The chip on this module is not a standard I²C register device — it uses a command/response protocol where you must write a command byte first, then read the response. That's why all our raw reads return 0xFF — we're reading without first sending a command.

# check if I²C is enabled on pi: sudo raspi-config 
    # > Interface Options → I2C → Enable (reboot if changed)

# you should see the device at address 0x03 using sudo i2cdetect -y -a 1

import smbus2
import time

bus = smbus2.SMBus(1)
ADDR = 0x03

def read():
    try:
        write = smbus2.i2c_msg.write(ADDR, [0x01])
        bus.i2c_rdwr(write)
        time.sleep(0.01)
        r = smbus2.i2c_msg.read(ADDR, 16)  # read 16 bytes instead of 8
        bus.i2c_rdwr(r)
        data = list(r)
        print(f"raw: {[hex(b) for b in data]}")
        return data
    except OSError as e:
        print(f"ERROR: {e}")

while True:
    read()
    time.sleep(1)