from smbus2 import SMBus
import time

# -----------------------------
# SET THESE FOR YOUR SENSOR
# -----------------------------
I2C_ADDRESS = 0x29      # change to your sensor address (check with i2cdetect)
REG_MSB = 0x14          # high-byte register address
REG_LSB = 0x15          # low-byte register address
# -----------------------------

bus = SMBus(1)

print("Reading raw I2C data continuously... Press CTRL+C to stop.\n")

while True:
    try:
        # Read MSB and LSB
        msb = bus.read_byte_data(I2C_ADDRESS, REG_MSB)
        lsb = bus.read_byte_data(I2C_ADDRESS, REG_LSB)

        # Combine into 16-bit number
        raw_value = (msb << 8) | lsb

        print(f"MSB: {msb:02X}, LSB: {lsb:02X}  -->  RAW: {raw_value}")

        time.sleep(0.1)  # read 10 times per second

    except KeyboardInterrupt:
        print("\nStopped by user.")
        break

    except Exception as e:
        print("Error:", e)
 







