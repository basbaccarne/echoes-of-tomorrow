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

def send_command(cmd, read_bytes=8):
    try:
        write = smbus2.i2c_msg.write(ADDR, [cmd])
        bus.i2c_rdwr(write)
        time.sleep(0.01)
        read = smbus2.i2c_msg.read(ADDR, read_bytes)
        bus.i2c_rdwr(read)
        return list(read)
    except OSError as e:
        return None

for cmd in [0x01, 0x02]:
    time.sleep(0.1)
    resp = send_command(cmd)
    print(f"cmd 0x{cmd:02X}: {[hex(b) for b in resp] if resp else 'ERROR'}")
    if resp:
        print(f"         binary: {[bin(b) for b in resp]}")