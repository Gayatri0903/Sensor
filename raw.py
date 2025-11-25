import smbus2
import time

I2C_ADDR = 0x29
bus = smbus2.SMBus(1)

# --------- Low-level helpers ----------
def write_reg(reg, val):
    bus.write_byte_data(I2C_ADDR, reg, val)

def read_reg(reg):
    return bus.read_byte_data(I2C_ADDR, reg)

def read16(reg):
    high = read_reg(reg)
    low  = read_reg(reg + 1)
    return (high << 8) | low

# --------- Sensor initialization ----------
def start_continuous():
    write_reg(0x00, 0x02)   # SYSRANGE_START = continuous back-to-back
    time.sleep(0.01)

# --------- Read raw distance ----------
def read_distance_mm():
    # Wait for “new sample ready”
    while True:
        status = read_reg(0x13)
        if status & 0x07:     # bit0 = ready, bit1/2 = no-error
            break
        time.sleep(0.002)

    # Raw distance = RESULT_RANGE_STATUS + 10 → 0x14 + 0x0A = 0x1E
    dist = read16(0x1E)

    # Clear the interrupt
    write_reg(0x0B, 0x01)

    return dist


# --------- Main loop ----------
print("VL53L0X in continuous mode")
start_continuous()
print("Reading distance...")

while True:
    try:
        d = read_distance_mm()
        print("Distance:", d, "mm")
        time.sleep(0.02)  # 20 ms → ~50 Hz
    except KeyboardInterrupt:
        print("Stopping...")
        break
    except Exception as e:
        print("I2C Error:", e)
        time.sleep(0.1)
