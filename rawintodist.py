import smbus2
import time

I2C_ADDR = 0x29
bus = smbus2.SMBus(1)

def write(reg, val):
    bus.write_byte_data(I2C_ADDR, reg, val)

def read(reg):
    return bus.read_byte_data(I2C_ADDR, reg)

def init_sensor():
    # Mandatory reset
    write(0x00, 0x00)
    time.sleep(0.01)

    # Load default tuning values (ST recommended)
    write(0x88, 0x00)
    write(0x80, 0x01)
    write(0xFF, 0x01)
    write(0x00, 0x00)
    write(0x91, 0x3C)   # tuning value from your dump
    write(0x00, 0x01)
    write(0xFF, 0x00)
    write(0x80, 0x00)

    # Start continuous mode
    write(0x00, 0x04)

def read_distance():
    status = read(0x13)
    if (status & 0x07) == 0:
        return None  # No valid data

    # distance is at 0x1E and 0x1F in most configs
    lo = read(0x1E)
    hi = read(0x1F)
    dist = (hi << 8) | lo

    write(0x0B, 0x01)  # clear interrupt
    return dist

# ------------------------------- MAIN LOOP
init_sensor()
print("VL53L0X ready!")

while True:
    d = read_distance()
    if d is not None:
        print("Distance:", d, "mm")
    else:
        print("Waiting ...")

    time.sleep(0.05)