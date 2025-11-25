import smbus2
import time

I2C_ADDR = 0x29
bus = smbus2.SMBus(1)

def write_reg(address, value):
    bus.write_byte_data(I2C_ADDR, address, value)

def read_reg(address):
    return bus.read_byte_data(I2C_ADDR, address)

def read_word(address):
    high = bus.read_byte_data(I2C_ADDR, address)
    low = bus.read_byte_data(I2C_ADDR, address + 1)
    return (high << 8) | low

# -------------------------
# SENSOR BOOT + RESET
# -------------------------
def sensor_init():
    # Soft reset
    write_reg(0xBF, 0x00)
    time.sleep(0.01)
    write_reg(0xBF, 0x01)
    time.sleep(0.01)

    # Mandatory internal tuning
    write_reg(0x88, 0x00)  
    write_reg(0x80, 0x01)
    write_reg(0xFF, 0x01)
    write_reg(0x00, 0x00)
    write_reg(0x91, read_reg(0x91))   # load tuning value
    write_reg(0x00, 0x01)
    write_reg(0xFF, 0x00)
    write_reg(0x80, 0x00)

    # Enable single-range mode
    write_reg(0x00, 0x01)  # SYSRANGE_START → single shot

# -------------------------
# READ RAW DISTANCE
# -------------------------
def read_distance_mm():

    # Start a single range measurement
    write_reg(0x00, 0x01)

    # Wait for new sample ready (RESULT_INTERRUPT_STATUS bit 2)
    while (read_reg(0x13) & 0x07) == 0:
        time.sleep(0.002)

    # Raw distance (RESULT_RANGE_STATUS block)
    dist = read_reg(0x1E)  # depending on variant
    if dist == 0:
        return None

    # Clear interrupt
    write_reg(0x0B, 0x01)

    return dist

# --------------------
# MAIN LOOP
# --------------------
sensor_init()

print("Reading distance...")
while True:
    d = read_distance_mm()
    if d is None:
        print("Invalid / no target detected")
    else:
        print("Distance:", d, "mm")
    time.sleep(0.1)