import smbus2
import time

bus = smbus2.SMBus(1)
I2C_ADDR = 0x29

def write_reg(reg, val):
    bus.write_byte_data(I2C_ADDR, reg, val)

def read_reg16(reg):
    high = bus.read_byte_data(I2C_ADDR, reg)
    low  = bus.read_byte_data(I2C_ADDR, reg+1)
    return (high << 8) | low

def sensor_init():
    write_reg(0x00, 0x00)   # SYSRANGE_START = idle

    # enable only final range sequence (required!)
    write_reg(0x01, 0x01)

    # set VCSEL period (safe value)
    write_reg(0x70, 14)

    # clear interrupt
    write_reg(0x0B, 0x01)

def read_distance_mm():
    # single shot start
    write_reg(0x00, 0x01)

    # wait for measurement ready
    while (bus.read_byte_data(I2C_ADDR, 0x13) & 0x07) == 0:
        time.sleep(0.005)

    dist = read_reg16(0x14)

    # clear interrupt
    write_reg(0x0B, 0x01)

    return dist

sensor_init()
print("VL53L0X ready!")

while True:
    d = read_distance_mm()
    print("Distance:", d, "mm")
    time.sleep(0.1)
