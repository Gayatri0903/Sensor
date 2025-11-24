import smbus2
import time

bus = smbus2.SMBus(1)
address = 0x29  # VL53L0X default

# Start ranging
bus.write_byte_data(address, 0x00, 0x01)

while True:
    # Check if data ready
    if bus.read_byte_data(address, 0x14) == 0x04:

        msb = bus.read_byte_data(address, 0x1E)
        lsb = bus.read_byte_data(address, 0x1F)

        distance = (msb << 8) | lsb

        print("Distance:", distance, "mm")

        # Clear interrupt
        bus.write_byte_data(address, 0x0B, 0x01)

    time.sleep(5)