import smbus2
import time

I2C_ADDR = 0x29
bus = smbus2.SMBus(1)

def write_reg(reg, val):
    bus.write_byte_data(I2C_ADDR, reg, val)

def read16(reg):
    high = bus.read_byte_data(I2C_ADDR, reg)
    low = bus.read_byte_data(I2C_ADDR, reg + 1)
    return (high << 8) | low

def sensor_start_continuous():
    """
    Put VL53L0X into continuous ranging mode.
    IMPORTANT: Sensor will NOT update distance unless continuous mode is enabled.
    """

    write_reg(0x00, 0x00)   # SYSRANGE_START → stop/idle
    time.sleep(0.01)

    write_reg(0x01, 0x02)   # SYSTEM_SEQUENCE_CONFIG = continuous
    time.sleep(0.01)

    write_reg(0x00, 0x02)   # SYSRANGE_START = Back-to-back continuous mode
    time.sleep(0.01)

    print("VL53L0X in continuous mode")

def read_distance_mm():
    """
    Read RAW distance from internal register.
    """

    # Wait for new sample
    while True:
        status = bus.read_byte_data(I2C_ADDR, 0x13)  # RESULT_INTERRUPT_STATUS
        if status & 0x07:   # any 'new data ready' flag
            break
        time.sleep(0.002)

    # raw distance is at 0x1E & 0x1F
    distance = read16(0x1E)

    # Clear interrupt
    write_reg(0x0B, 0x01)

    return distance

# --------- MAIN ----------
sensor_start_continuous()

print("Reading distance...")

while True:
    try:
        dist = read_distance_mm
