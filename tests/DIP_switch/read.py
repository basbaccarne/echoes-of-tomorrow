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

def read_switches():
    try:
        # Read 10 bytes with no register (pure sequential read)
        msg = smbus2.i2c_msg.read(ADDR, 10)
        bus.i2c_rdwr(msg)
        data = list(msg)
        return data
    except OSError as e:
        print(f"ERROR: {e}")
        return None

while True:
    data = read_switches()
    if data:
        print(f"raw: {[hex(b) for b in data]}")
        # Event header is bytes 0-3
        has_event = (data[0] | data[1]<<8 | data[2]<<16 | data[3]<<24) & 0x80000000
        print(f"has_event: {bool(has_event)}")
        # Switch states are bytes 4-9
        print("─" * 30)
        for i in range(6):
            state = "ON " if not (data[4+i] & 0x01) else "OFF"
            print(f"  Switch {i+1}: {state}  (raw byte: {hex(data[4+i])})")
    time.sleep(1)