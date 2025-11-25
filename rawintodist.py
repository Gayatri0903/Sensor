import smbus2
import time

I2C_ADDR = 0x29
bus = smbus2.SMBus(1)

def write_reg(reg, val):
    bus.write_byte_data(I2C_ADDR, reg, val)

def read_reg(reg):
    return bus.read_byte_data(I2C_ADDR, reg)

# ------------------------------------------------------------
# INITIALIZE VL53L0X
# ------------------------------------------------------------
def sensor_init():
    write_reg(0x00, 0x01)     # start continuous ranging
    time.sleep(0.01)

# ------------------------------------------------------------
# READ RAW DISTANCE
# ------------------------------------------------------------
def read_raw_distance():
    status = read_reg(0x13)        # RESULT_INTERRUPT_STATUS

    # bit 0 == new measurement ready
    if (status & 0x07) == 0:
        return None  # not ready yet

    # distance is stored at registers 0x1E + 0x1F
    high = read_reg(0x1E)
    low  = read_reg(0x1F)

    distance_mm = (high << 8) | low

    write_reg(0x0B, 0x01)          # clear interrupt

    return distance_mm

# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------
sensor_init()
print("Reading raw distance continuously...\n")

while True:
    dist = read_raw_distance()
    if dist is not None:
        print("Distance:", dist, "mm")
    time.sleep(0.05)
