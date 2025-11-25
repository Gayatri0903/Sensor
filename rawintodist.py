from smbus2 import SMBus
import time

ADDR = 0x29  # VL53L0X default I2C address
bus = SMBus(1)

# Helpers
def write(reg, value):
    bus.write_byte_data(ADDR, reg, value)

def read(reg):
    return bus.read_byte_data(ADDR, reg)

def read16(reg):
    high = bus.read_byte_data(ADDR, reg)
    low = bus.read_byte_data(ADDR, reg + 1)
    return (high << 8) + low

# Minimal init sequence from ST application notes
def vl53l0x_init():
    try:
        # Sensor boot
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
        print("❌ Initialization error:", e)
        return False

def start_ranging():
    write(0x00, 0x01)  # SYSRANGE_START

def get_distance():
    # Wait for measurement ready
    while (read(0x13) & 0x07) == 0:
        time.sleep(0.002)

    distance = read16(0x14)  # RESULT_RANGE_STATUS + 10

    write(0x0B, 0x01)  # clear interrupt

    return distance

# ---- MAIN PROGRAM ----
if __name__ == "__main__":
    print("Initializing VL53L0X...")

    if not vl53l0x_init():
        print("❌ Failed to initialize VL53L0X.")
        exit()

    print("✅ Sensor initialized. Starting ranging...\n")

    start_ranging()

    try:
        while True:
            dist = get_distance()
            print(f"Distance: {dist} mm")
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nStopped.")