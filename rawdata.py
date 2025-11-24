import smbus2
import time

bus = smbus2.SMBus(1)
address = 0x29  # VL53L0X

# Start measurement (VL53L0X needs init)
bus.write_byte_data(address, 0x00, 0x01)  # sysrange start

while True:
    # Read RAW result block (0x14 → 14 bytes)
    raw = bus.read_i2c_block_data(address, 0x14, 14)

    print("RAW DATA:", raw)

    time.sleep(0.1)