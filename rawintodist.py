import smbus
import time

I2C_ADDR = 0x29
bus = smbus.SMBus(1)

# Write a single register
def write(reg, val):
    bus.write_byte_data(I2C_ADDR, reg, val)

# Read a single register
def read(reg):
    return bus.read_byte_data(I2C_ADDR, reg)

def vl6180x_init():
    try:
        # Reset
        write(0x0200, 0x01)
        time.sleep(0.01)

        # Mandatory initialization settings for VL6180X
        write(0x0207, 0x01)
        write(0x0208, 0x01)
        write(0x0096, 0x00)
        write(0x0097, 0xFD)
        write(0x00E3, 0x00)
        write(0x00E4, 0x04)
        write(0x00E5, 0x02)
        write(0x00E6, 0x01)
        write(0x00E7, 0x03)
        write(0x00F5, 0x02)
        write(0x00D9, 0x05)
        write(0x00DB, 0xCE)
        write(0x00DC, 0x03)
        write(0x00DD, 0xF8)
        write(0x009F, 0x00)
        write(0x00A3, 0x3C)
        write(0x00B7, 0x00)
        write(0x00BB, 0x3C)
        write(0x00B2, 0x09)

        return True

    except Exception as e:
        print("Init error:", e)
        return False


def read_distance():
    # Start a range measurement
    write(0x018, 0x01)

    # Wait for result ready
    time.sleep(0.01)

    # Read range value (RAW)
    raw = read(0x062)

    # Clear interrupt
    write(0x015, 0x07)

    return raw


print("Initializing VL6180X...")

if not vl6180x_init():
    print("❌ SENSOR INIT FAILED")
    exit()

print("✔ Sensor Ready!")

while True:
    dist = read_distance()
    print("Distance:", dist, "mm")
    time.sleep(0.1)