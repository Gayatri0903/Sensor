import smbus2
import time

I2C_ADDR = 0x29
bus = smbus2.SMBus(1)

# ---- Helper functions ----
def write_reg(reg, val):
    bus.write_byte_data(I2C_ADDR, reg, val)

def read_reg(reg):
    return bus.read_byte_data(I2C_ADDR, reg)

def read16(reg):
    high = read_reg(reg)
    low  = read_reg(reg + 1)
    return (high << 8) | low

# ---- Sensor init for continuous mode ----
def vl53l0x_init_continuous():
    # Soft reset
    write_reg(0x00, 0x00)
    time.sleep(0.01)

    # Start continuous ranging
    write_reg(0x00, 0x02)        # SYSRANGE_START = 2 → continuous mode
    time.sleep(0.01)

# ---- Read measurement ----
def read_distance_mm():
    # Wait for a new sample ready
    while True:
        status = read_reg(0x14)      # RESULT_RANGE_STATUS
        if status & 0x01:            # bit0 = new sample
            break
        time.sleep(0.002)

    # Distance = registers 0x1E + 0x1F
    dist = read16(0x1E)

    # Clear interrupt
    write_reg(0x0B, 0x01)

    return dist

# ---- MAIN ----
vl53l0x_init_continuous()
print("VL53L0X running in continuous mode...\n")

while True:
    try:
        dist = read_distance_mm()
        print("Distance:", dist, "mm")
        time.sleep(0.05)

    except Exception as e:
        print("I2C Error:", e)
        time.sleep(0.1)
