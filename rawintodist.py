import smbus2
import time

bus = smbus2.SMBus(1)
addr = 0x29

# ---- VL53L0X Simple Initialization ----
def write(reg, value):
    bus.write_byte_data(addr, reg, value)

def read_byte(reg):
    return bus.read_byte_data(addr, reg)

def read_word(reg):
    msb = bus.read_byte_data(addr, reg)
    lsb = bus.read_byte_data(addr, reg + 1)
    return (msb << 8) | lsb

# Enable sensor (mandatory)
write(0x88, read_byte(0x88) | 0x01)

# Start continuous ranging
write(0x80, 0x01)
write(0xFF, 0x01)
write(0x00, 0x00)
write(0x91, read_byte(0x91))
write(0x00, 0x01)
write(0xFF, 0x00)
write(0x80, 0x00)

# Command: continuous mode
write(0x00, 0x04)

print("VL53L0X running...")

# ---- Continuous Read Loop ----
while True:
    distance_mm = read_word(0x14)  # Correct distance register
    distance_cm = distance_mm / 10.0

    print(f"Distance: {distance_mm} mm   {distance_cm:.2f} cm")

    time.sleep(0.05)  # 20 Hz