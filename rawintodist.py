import smbus2
import time

I2C_ADDR = 0x29
bus = smbus2.SMBus(1)

# --- Simple I2C helpers ---
def read_reg(reg):
    return bus.read_byte_data(I2C_ADDR, reg)

def read_word(reg):
    # Sensor stores MSB first
    high = bus.read_byte_data(I2C_ADDR, reg)
    low  = bus.read_byte_data(I2C_ADDR, reg + 1)
    return (high << 8) | low

# --- Start sensor in single-shot mode ---
def start_single_measurement():
    bus.write_byte_data(I2C_ADDR, 0x00, 0x01)

# --- Read raw distance from RESULT registers ---
def read_raw_distance():
    # 1) Start new measurement
    start_single_measurement()

    # 2) Wait for RESULT_INTERRUPT_STATUS bit (bit 0)
    while True:
        status = read_reg(0x13)
        if status & 0x01:   # New Sample Ready
            break
        time.sleep(0.001)

    # 3) Read distance (RESULT_RANGE_MM at 0x1E)
    distance_mm = read_word(0x1E)

    # 4) Clear interrupt
    bus.write_byte_data(I2C_ADDR, 0x0B, 0x01)

    return distance_mm

# --- Main loop ---
print("Reading raw distance continuously...\n")

while True:
    dist = read_raw_distance()
    print(f"Distance: {dist} mm")
    time.sleep(0.05)