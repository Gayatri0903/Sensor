from smbus2 import SMBus
import time

I2C_ADDRESS = 0x29
REGISTER = 0x00       # starting register
NUM_BYTES = 16        # how many bytes to read

bus = SMBus(1)

print("Reading block data...\n")

try:
    while True:
        data = bus.read_i2c_block_data(I2C_ADDRESS, REGISTER, NUM_BYTES)
        print(" ".join(f"{b:02X}" for b in data))
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nStopped.")