from smbus2 import SMBus
import time

# -------------------------------
# EDIT THESE FOR YOUR SENSOR
# -------------------------------
I2C_ADDRESS = 0x29    # change to your sensor I2C address
REG_START   = 0x00    # starting register to read from
NUM_BYTES   = 8       # how many raw bytes you want to read
# -------------------------------

bus = SMBus(1)

print("Reading RAW I2C bytes... Press CTRL+C to stop.\n")

try:
    while True:
        # Read a block of raw bytes
        raw = bus.read_i2c_block_data(I2C_ADDRESS, REG_START, NUM_BYTES)

        # Print raw bytes in hex
        print("RAW:", " ".join(f"{b:02X}" for b in raw))

        time.sleep(0.1)   # 10 times per second

except KeyboardInterrupt:
    print("\nStopped.")