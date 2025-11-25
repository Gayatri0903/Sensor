import smbus
import time

I2C_ADDR = 0x29
bus = smbus.SMBus(1)

print("Dumping 0x00–0xFF:")
for reg in range(0x00, 0x100):
    try:
        val = bus.read_byte_data(I2C_ADDR, reg)
        print(f"0x{reg:02X}: 0x{val:02X}")
    except:
        print(f"0x{reg:02X}: --")