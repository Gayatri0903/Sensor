import smbus2
import time

I2C_ADDR = 0x29
bus = smbus2.SMBus(1)

def init_sensor():
    # Put sensor in continuous ranging mode
    bus.write_byte_data(I2C_ADDR, 0x00, 0x01)   # SYSRANGE_START = 0x01
    time.sleep(0.01)

def read16(reg):
    high = bus.read_byte_data(I2C_ADDR, reg)
    low  = bus.read_byte_data(I2C_ADDR, reg + 1)
    return (high << 8) | low

def read_distance_mm():
    # Wait for new sample
    while True:
        status = bus.read_byte_data(I2C_ADDR, 0x14)
        if status & 0x01:
            break
        time.sleep(0.001)

    # Distance register (16-bit)
    dist = read16(0x1E)

    # Clear interrupt
    bus.write_byte_data(I2C_ADDR, 0x0B, 0x01)

    return dist

print("Starting VL53L0X continuous ranging...")
init_sensor()

while True:
    d = read_distance_mm()
    print("Distance:", d, "mm")
    time.sleep(0.02)
