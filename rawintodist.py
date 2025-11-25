import smbus2
import time

bus = smbus2.SMBus(1)
I2C_ADDR = 0x29

# --- Write a register ---
def write_reg(reg, value):
    bus.write_byte_data(I2C_ADDR, reg, value)

# --- Read a register ---
def read_reg(reg):
    return bus.read_byte_data(I2C_ADDR, reg)

# --- Start a single measurement ---
def start_measurement():
    write_reg(0x00, 0x01)   # SYSRANGE_START – start measurement

# --- Read raw distance ---
def read_raw_distance():
    # Wait for device to assert "measurement ready"
    # RESULT_INTERRUPT_STATUS = 0x13, bit0 = new sample ready
    while True:
        status = read_reg(0x13)
        if status & 0x07:       # any valid new-sample flag
            break
        print("Waiting for measurement...")
        time.sleep(0.01)

    # Distance result registers
    high = read_reg(0x1E)
    low  = read_reg(0x1F)

    # Convert raw 16-bit value → mm
    distance_mm = (high << 8) | low

    # Clear interrupt
    write_reg(0x0B, 0x01)

    return distance_mm

# --- MAIN LOOP ---
print("VL53L0X — raw distance reader")

while True:
    start_measurement()
    dist = read_raw_distance()
    print("Distance:", dist, "mm")
    time.sleep(0.05)