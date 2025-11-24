from smbus2 import SMBus
import time

bus = SMBus(1)
address = 0x29          # or 0x52 depending on your module

DIST_MSB = 0x14
DIST_LSB = 0x15

print("Reading distance continuously... Press CTRL+C to stop")

while True:
    try:
        msb = bus.read_byte_data(address, DIST_MSB)
        lsb = bus.read_byte_data(address, DIST_LSB)

        distance_mm = (msb << 8) | lsb

        print("Distance:", distance_mm, "mm")

        time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopped by user.")
        break