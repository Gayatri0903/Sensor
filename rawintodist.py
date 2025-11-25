import smbus2
import time

I2C_ADDR = 0x29
bus = smbus2.SMBus(1)

def read16(reg):
    """Read 16-bit big-endian value"""
    high = bus.read_byte_data(I2C_ADDR, reg)
    low = bus.read_byte_data(I2C_ADDR, reg + 1)
    return (high << 8) | low

def read_distance_mm():
    """Read distance from VL53L0X raw registers"""
    # 1) Wait for a new measurement
    while True:
        status = bus.read_byte_data(I2C_ADDR, 0x14)
        if status & 0x01:   # bit0 = New sample ready
            break
        time.sleep(0.005)

    # 2) Distance is at RESULT_RANGE_STATUS + 10 = 0x14 + 0x0A = 0x1E
    dist = read16(0x1E)

    # 3) Clear interrupt (acknowledge reading)
    bus.write_byte_data(I2C_ADDR, 0x0B, 0x01)

    return dist

print("Reading distance from VL53L0X...")

while True:
    try:
        d = read_distance_mm()
        print("Distance:", d, "mm")
    except Exception as e:
        print("I2C Error:", e)

    time.sleep(0.05)
