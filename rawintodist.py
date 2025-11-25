import smbus2
import time

I2C_ADDR = 0x29
bus = smbus2.SMBus(1)

def write_reg(reg, value):
    bus.write_byte_data(I2C_ADDR, reg, value)

def read_reg(reg):
    return bus.read_byte_data(I2C_ADDR, reg)

def read_word(reg):
    high = read_reg(reg)
    low = read_reg(reg+1)
    return (high << 8) | low

# ---------------------------
# VL6180X INIT SEQUENCE
# ---------------------------

def sensor_init():
    # Recommended settings from ST AN4545
    write_reg(0x0207, 0x01)
    write_reg(0x0208, 0x01)
    write_reg(0x0096, 0x00)
    write_reg(0x0097, 0xFD)
    write_reg(0x00E3, 0x00)
    write_reg(0x00E4, 0x04)
    write_reg(0x00E5, 0x02)
    write_reg(0x00E6, 0x01)
    write_reg(0x00E7, 0x03)
    write_reg(0x00F5, 0x02)
    write_reg(0x00D9, 0x05)
    write_reg(0x00DB, 0xCE)
    write_reg(0x00DC, 0x03)
    write_reg(0x00DD, 0xF8)
    write_reg(0x009F, 0x00)
    write_reg(0x00A3, 0x3C)
    write_reg(0x00B7, 0x00)
    write_reg(0x00BB, 0x3C)
    write_reg(0x00B2, 0x09)
    write_reg(0x00CA, 0x09)
    write_reg(0x0198, 0x01)
    write_reg(0x01B0, 0x17)
    write_reg(0x01AD, 0x00)
    write_reg(0x00FF, 0x05)
    write_reg(0x0100, 0x05)
    write_reg(0x0199, 0x05)
    write_reg(0x01A6, 0x1B)
    write_reg(0x01AC, 0x3E)
    write_reg(0x01A7, 0x1F)
    write_reg(0x010A, 0x30)
    write_reg(0x003F, 0x46)
    write_reg(0x01A4, 0x05)
    write_reg(0x01A3, 0x3C)
    write_reg(0x01B1, 0x00)
    write_reg(0x01B2, 0x00)
    write_reg(0x01B3, 0x00)
    write_reg(0x01B4, 0x00)
    write_reg(0x01B5, 0x00)
    write_reg(0x01B6, 0x00)

    # enable sensor
    write_reg(0x010A, 0x30)

    # configure interrupts (new sample ready)
    write_reg(0x0A, 0x04)

    print("VL6180X initialised")

# ---------------------------
# READ DISTANCE
# ---------------------------

def read_distance_mm():
    write_reg(0x00, 0x01)  # start single shot

    # wait for result
    while (read_reg(0x04) & 0x01) == 0:
        time.sleep(0.001)

    dist = read_reg(0x62)  # RANGE value

    write_reg(0x0B, 0x07)  # clear interrupts

    return dist


# ---------------------------
# MAIN
# ---------------------------

sensor_init()

while True:
    d = read_distance_mm()
    print("Distance:", d, "mm")
    time.sleep(0.1)