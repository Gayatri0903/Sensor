from smbus2 import SMBus
import time

I2C_ADDRESS = 0x29
REGISTER = 0x00

bus = SMBus(1)

print("Reading raw I2C data... Press CTRL+C to stop.\n")

try:
    while True:
        raw_byte = bus.read_byte_data(I2C_ADDRESS, REGISTER)
        print(f"Register 0x{REGISTER:02X} -> Raw = {raw_byte:02X} ({raw_byte})")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopped by user.")