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

# Command IDs from the Arduino library source
CMDID_GET_DEV_ID      = 0x00
CMDID_GET_SWITCH_STATUS = 0x02  # returns 6 bytes, one per switch

def send_command(cmd):
    """Write a command byte, then read the response"""
    try:
        # Step 1: write the command
        write = smbus2.i2c_msg.write(ADDR, [cmd])
        bus.i2c_rdwr(write)
        time.sleep(0.002)  # 2ms for chip to prepare response
        # Step 2: read 8 bytes back
        read = smbus2.i2c_msg.read(ADDR, 8)
        bus.i2c_rdwr(read)
        return list(read)
    except OSError as e:
        print(f"ERROR: {e}")
        return None

print("-- Device ID --")
resp = send_command(CMDID_GET_DEV_ID)
print(f"raw: {[hex(b) for b in resp] if resp else 'failed'}")

print("\n-- Switch status (all off) --")
resp = send_command(CMDID_GET_SWITCH_STATUS)
if resp:
    print(f"raw: {[hex(b) for b in resp]}")
    for i in range(6):
        state = "ON" if not (resp[i] & 0x01) else "OFF"
        print(f"  Switch {i+1}: {state}")