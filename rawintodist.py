import smbus2
import time

# --- EDIT THESE TO MATCH YOUR SENSOR ---
I2C_ADDR  = 0x40   # device address
REG_MSB   = 0x00   # register for MSB
REG_LSB   = 0x01   # register for LSB
SCALE_MM  = 1.0    # raw → mm (example: 1 raw = 1 mm)
# ---------------------------------------

bus = smbus2.SMBus(1)  # I2C bus number (1 for Raspberry Pi)

while True:
    try:
        # Read two bytes from sensor
        msb = bus.read_byte_data(I2C_ADDR, REG_MSB)
        lsb = bus.read_byte_data(I2C_ADDR, REG_LSB)

        # Combine to 16-bit raw value
        raw = (msb << 8) | lsb

        # Convert to distance
        distance_mm = raw * SCALE_MM
        distance_cm = distance_mm / 10.0

        print(f"Raw: {raw}   Distance: {distance_mm:.1f} mm   {distance_cm:.2f} cm")

    except Exception as e:
        print("I2C error:", e)

    time.sleep(0.1)  # 10 readings per second