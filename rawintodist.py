import smbus2
import time

# I2C settings (change to match your sensor)
I2C_BUS = 1
I2C_ADDR = 0x40       # sensor address
REG_MSB = 0x00        # high byte register
REG_LSB = 0x01        # low byte register

# Conversion factor (example: each raw unit = 1 mm)
SCALE_MM = 1.0        # change according to your sensor's datasheet

bus = smbus2.SMBus(I2C_BUS)

def read_raw16():
    """Reads two bytes (MSB + LSB) and returns a 16-bit integer."""
    msb = bus.read_byte_data(I2C_ADDR, REG_MSB)
    lsb = bus.read_byte_data(I2C_ADDR, REG_LSB)
    raw = (msb << 8) | lsb
    return raw

while True:
    raw = read_raw16()

    distance_mm = raw * SCALE_MM
    distance_cm = distance_mm / 10.0

    print(f"Raw: {raw}   Distance: {distance_mm:.1f} mm   ({distance_cm:.2f} cm)")
    
    time.sleep(0.2)   # 5 readings per second