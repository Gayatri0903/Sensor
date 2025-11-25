from smbus2 import SMBus
import time

ADDR = 0x29                   # VL53L0X default address
bus = SMBus(1)

# ---- BASIC I2C HELPERS ----
def write(reg, val):
    try:
        bus.write_byte_data(ADDR, reg, val)
        return True
    except:
        return False

def read(reg):
    try:
        return bus.read_byte_data(ADDR, reg)
    except:
        return None

def read16(reg):
    try:
        high = bus.read_byte_data(ADDR, reg)
        low = bus.read_byte_data(ADDR, reg + 1)
        return (high << 8) | low
    except:
        return None

# ---- SENSOR INIT ----
def init_sensor():
    ok = True
    ok &= write(0x88, (read(0x88) or 0) | 0x01)
    ok &= write(0x80, 0x01)
    ok &= write(0xFF, 0x01)
    ok &= write(0x00, 0x00)
    tmp = read(0x91)
    ok &= write(0x00, 0x01)
    ok &= write(0xFF, 0x00)
    ok &= write(0x80, 0x00)
    return ok

def start_ranging():
    write(0x00, 0x01)

def get_distance():
    # Wait for measurement ready
    r = read(0x13)
    if r is None:
        return None

    if (r & 0x07) == 0:
        return None

    dist = read16(0x14)
    write(0x0B, 0x01)  # Clear interrupt

    return dist


# ---- MAIN LOOP ----
print("Initializing VL53L0X...")

if not init_sensor():
    print("⚠️ Sensor not acknowledged. Reading will retry anyway.")
else:
    print("✅ Sensor initialized.")

start_ranging()

print("\n--- Continuous Distance Readings ---\n")

while True:
    dist = get_distance()

    if dist is None:
        print("⚠️ No data (sensor not responding)...")
    else:
        print(f"Distance: {dist} mm")

    time.sleep(0.05)