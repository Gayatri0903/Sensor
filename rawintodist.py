import time
from smbus2 import SMBus

I2C_ADDR = 0x29
bus = SMBus(1)

# ---------- BASIC REGISTER ACCESS ----------
def write_reg(reg, value):
    bus.write_byte_data(I2C_ADDR, reg, value)

def read_reg(reg):
    return bus.read_byte_data(I2C_ADDR, reg)

def read_word(reg):
    high = read_reg(reg)
    low  = read_reg(reg+1)
    return (high << 8) | low


# ---------- SENSOR INITIALIZATION ----------
def sensor_init():
    model = read_reg(0xC0)
    revision = read_reg(0xC2)

    print(f"VL53L0X Model: {hex(model)}, Revision: {hex(revision)}")

    if model != 0xEE:
        print("WARNING: Unexpected Model ID! Check wiring.")
    else:
        print("VL53L0X detected.")

    # Soft reset
    write_reg(0x00, 0x00)
    time.sleep(0.1)

    # System Sequence Config – enable PreRange + FinalRange
    write_reg(0x01, 0xFF)

    # Set continuous mode timing
    write_reg(0x04, 0x08)  # Inter-measurement period
    write_reg(0x0A, 0x04)  # "New Sample Ready" interrupt

    # Clear interrupts
    write_reg(0x0B, 0x01)

    # Start continuous ranging
    write_reg(0x00, 0x02)
    print("Sensor started in continuous mode.")


# ---------- READ RAW + DISTANCE ----------
def read_distance():
    status = read_reg(0x13) & 0x07
    if status != 0x04:   # 0x04 = "data ready"
        return None, None

    # RAW registers from datasheet
    ambient_raw = read_word(0xBC)
    signal_raw  = read_word(0xC0)

    # Final distance
    distance_mm = read_word(0x14)

    # Clear interrupt for next measurement
    write_reg(0x0B, 0x01)

    return (ambient_raw, signal_raw, distance_mm)


# ---------- MAIN LOOP ----------
sensor_init()
print("Reading distance continuously...\n")

while True:
    ambient, signal, dist = read_distance()
    if dist is not None:
        print(f"Ambient Raw: {ambient} | Signal Raw: {signal} | Distance: {dist} mm")
    else:
        print("Waiting for new data...")
    time.sleep(0.05)