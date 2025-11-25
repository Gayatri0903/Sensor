import smbus2
import time

I2C_ADDR = 0x29
bus = smbus2.SMBus(1)

def write_reg(reg, val):
    bus.write_byte_data(I2C_ADDR, reg, val)

def read_reg(reg):
    return bus.read_byte_data(I2C_ADDR, reg)

def read16(reg):
    data = bus.read_i2c_block_data(I2C_ADDR, reg, 2)
    return (data[0] << 8) | data[1]

# ---- VL53L0X BASIC STARTUP ----
def vl53l0x_init():
    # Soft reset
    write_reg(0x00, 0x00)
    time.sleep(0.1)

    # Use default continuous ranging mode
    write_reg(0x80, 0x01)
    write_reg(0xFF, 0x01)
    write_reg(0x00, 0x00)
    
    # Mandatory registers (from ST API)
    write_reg(0x91, 0x3C)  # Phase calibration
    
    write_reg(0x00, 0x01)
    write_reg(0xFF, 0x00)
    write_reg(0x80, 0x00)

    print("VL53L0X ready!")

def start_ranging():
    write_reg(0x00, 0x01)  # SYSRANGE_START = single shot

def read_distance_mm():
    # Wait for data ready
    while (read_reg(0x13) & 0x07) == 0:
        time.sleep(0.001)

    dist = read16(0x1E)  # RESULT_RANGE_STATUS + 0x1E → distance register
    write_reg(0x0B, 0x01)  # SYSTEM_INTERRUPT_CLEAR
    return dist

# ---------------- MAIN ----------------
vl53l0x_init()

while True:
    start_ranging()
    time.sleep(0.025)
    d = read_distance_mm()
    print("Distance:", d, "mm")
    time.sleep(0.1)