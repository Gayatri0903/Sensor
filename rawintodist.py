from smbus2 import SMBus
import time

I2C_ADDR = 0x29
bus = SMBus(1)

def write_reg(reg, val):
    bus.write_byte_data(I2C_ADDR, reg, val)

def read_reg16(reg):
    high = bus.read_byte_data(I2C_ADDR, reg)
    low  = bus.read_byte_data(I2C_ADDR, reg + 1)
    return (high << 8) | low

def sensor_init():
    # Put sensor in continuous mode
    write_reg(0x00, 0x02)       # SYSRANGE_START = back-to-back continuous mode
    time.sleep(0.005)

def read_distance():
    status = bus.read_byte_data(I2C_ADDR, 0x14)

    if (status & 0x01) == 0:
        return None, None, None   # No range data ready

    # Raw signals:
    ambient = read_reg16(0xBC)       # RESULT_CORE_AMBIENT_WINDOW_EVENTS_RTN
    signal  = read_reg16(0xC0)       # RESULT_CORE_RANGING_TOTAL_EVENTS_RTN

    # Actual distance:
    distance = read_reg16(0x1E)      # RESULT_RANGE_MM (valid for VL53L0X)

    # Clear interrupt
    write_reg(0x0B, 0x01)

    return ambient, signal, distance

sensor_init()
print("VL53L0X running in continuous mode...\n")

while True:
    ambient, signal, dist = read_distance()

    if dist is None:
        print("Waiting for measurement...")
    else:
        print(f"Ambient={ambient} | Signal={signal} | Distance={dist} mm")

    time.sleep(0.05)