import smbus2
import time

bus = smbus2.SMBus(1)
I2C_ADDR = 0x29

def write_reg(reg, value):
    bus.write_byte_data(I2C_ADDR, reg, value)

def read_reg(reg):
    return bus.read_byte_data(I2C_ADDR, reg)

def read_reg16(reg):
    high = read_reg(reg)
    low = read_reg(reg + 1)
    return (high << 8) | low

def sensor_init():
    # Mandatory settings from ST AN4545
    write_reg(0x020, 0x00)  # SYSRANGE__START
    write_reg(0x010, 0x00)  # SYSTEM__MODE_GPIO0
    write_reg(0x011, 0x00)
    write_reg(0x014, 0x00)

    # Fresh out of reset recommended configuration
    write_reg(0x016, 0x07)
    write_reg(0x017, 0x01)
    write_reg(0x018, 0x07)
    write_reg(0x019, 0x01)

    print("Init OK")

def get_distance():
    write_reg(0x00, 0x01)          # start single range measurement
    time.sleep(0.01)

    status = read_reg(0x4F)
    distance = read_reg(0x62)     # RESULT__RANGE_MM

    # Clear interrupt
    write_reg(0x0B, 0x07)

    return distance

sensor_init()

while True:
    dist = get_distance()
    print("Distance:", dist, "mm")
    time.sleep(0.1)
