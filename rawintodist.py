import smbus2
import time

I2C_ADDR = 0x29
bus = smbus2.SMBus(1)

def write_reg(reg, value):
    bus.write_byte_data(I2C_ADDR, reg, value)

def read_reg(reg):
    return bus.read_byte_data(I2C_ADDR, reg)

def read_word(reg):
    high = bus.read_byte_data(I2C_ADDR, reg)
    low  = bus.read_byte_data(I2C_ADDR, reg + 1)
    return (high << 8) | low

def init_vl53l0x():
    try:
        # Basic safe init sequence
        write_reg(0x88, read_reg(0x88) | 0x01)
        write_reg(0x80, 0x01)
        write_reg(0xFF, 0x01)
        write_reg(0x00, 0x00)
        write_reg(0x91, 0x3C)  # default reference SPAD
        write_reg(0x00, 0x01)
        write_reg(0xFF, 0x00)
        write_reg(0x80, 0x00)
        return True

    except Exception as e:
        print("Init error:", e)
        return False

def start_ranging():
    write_reg(0x00, 0x01)  # Start measurement

def data_ready():
    # Range status: bit 0 = new measurement ready
    status = read_reg(0x13)
    return bool(status & 0x07)

def clear_interrupt():
    write_reg(0x0B, 0x01)

def read_distance():
    # Raw distance result registers
    dist = read_word(0x14)
    return dist  # already in mm

# -----------------------------
#       MAIN PROGRAM
# -----------------------------
print("Initializing sensor...")

if not init_vl53l0x():
    print("❌ SENSOR INIT FAILED")
    exit()

print("✔ Sensor initialized")
start_ranging()

while True:
    try:
        if data_ready():
            raw_mm = read_distance()
            clear_interrupt()
            print("Distance:", raw_mm, "mm")
        else:
            print("Waiting...")
        time.sleep(0.05)

    except Exception as e:
        print("Read error:", e)
        time.sleep(0.5)