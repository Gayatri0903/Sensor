from smbus2 import SMBus
import time

I2C_ADDR = 0x29
bus = SMBus(1)

# -------------------------------
# Low-level helpers
# -------------------------------
def write(reg, val):
    bus.write_byte_data(I2C_ADDR, reg, val)

def read(reg):
    return bus.read_byte_data(I2C_ADDR, reg)

def read16(reg):
    data = bus.read_i2c_block_data(I2C_ADDR, reg, 2)
    return (data[0] << 8) | data[1]

# -------------------------------
# VL53L0X Initialization Sequence
# -------------------------------
def vl53l0x_init():
    # Check model ID
    model = read(0xC0)
    if model != 0xEE:
        print("Wrong Model ID:", hex(model))
        return False
    
    # Fresh device boot
    write(0x88, read(0x88) | 0x01)

    write(0x80, 0x01)
    write(0xFF, 0x01)
    write(0x00, 0x00)
    write(0xFF, 0x00)
    write(0x80, 0x00)

    # Set continuous mode
    write(0x01, 0x02)   # max convergence time
    write(0x00, 0x02)   # start continuous ranging

    time.sleep(0.05)
    return True

# -------------------------------
# Get distance (mm)
# -------------------------------
def get_distance_mm():
    # Wait for data ready
    if (read(0x13) & 0x07) == 0:
        return None

    # Read distance registers
    dist = read16(0x1E)

    # Clear interrupt
    write(0x0B, 0x01)

    return dist

# -------------------------------
# Main Loop
# -------------------------------
if not vl53l0x_init():
    print("Sensor failed to initialize.")
    exit()

print("VL53L0X running...\n")

while True:
    d = get_distance_mm()
    if d is not None:
        print(f"Distance: {d} mm   ({d/10.0:.1f} cm)")
    time.sleep(0.05)