from smbus2 import SMBus
import time

ADDR = 0x29
bus = SMBus(1)

# ---------------------------------------------------
# BASIC HELPERS
# ---------------------------------------------------
def write(reg, val):
    bus.write_byte_data(ADDR, reg, val)

def read(reg):
    return bus.read_byte_data(ADDR, reg)

def read16(reg):
    high = bus.read_byte_data(ADDR, reg)
    low = bus.read_byte_data(ADDR, reg + 1)
    return (high << 8) | low

# ---------------------------------------------------
# SIMPLE OFFICIAL INIT (NO COMPLEX SEQUENCES)
# ---------------------------------------------------
def init_vl53():
    try:
        # Mandatory boot sequence
        write(0x88, read(0x88) | 0x01)
        write(0x80, 0x01)
        write(0xFF, 0x01)
        write(0x00, 0x00)
        write(0x91, read(0x91))
        write(0x00, 0x01)
        write(0xFF, 0x00)
        write(0x80, 0x00)
        return True
    except Exception as e:
        print("Init error:", e)
        return False

# ---------------------------------------------------
# START ONE-TIME RANGING MEASUREMENT
# ---------------------------------------------------
def start_measurement():
    write(0x00, 0x01)

# ---------------------------------------------------
# READ RAW + CONVERT TO DISTANCE
# ---------------------------------------------------
def read_distance():
    # Wait until measurement is ready
    if (read(0x13) & 0x07) == 0:
        return None

    dist = read16(0x14)  # raw → mm
    write(0x0B, 0x01)    # clear interrupt
    return dist

# ---------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------
print("Initializing sensor...")

if not init_vl53():
    print("Sensor init failed.")
    exit()

print("Sensor ready.\n")
start_measurement()

while True:
    d = read_distance()

    if d is not None:
        print("Distance:", d, "mm")
    else:
        print("Waiting...")

    time.sleep(0.05)
