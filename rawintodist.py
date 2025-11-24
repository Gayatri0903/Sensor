import smbus2
import time

bus = smbus2.SMBus(1)
addr = 0x29

# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------
def write(reg, val):
    bus.write_byte_data(addr, reg, val)

def read(reg):
    return bus.read_byte_data(addr, reg)

def read_word(reg):
    high = bus.read_byte_data(addr, reg)
    low  = bus.read_byte_data(addr, reg + 1)
    return (high << 8) | low

# -------------------------------------------------
# MINIMAL VL53L0X STARTUP (NO 0x88 REQUIRED)
# -------------------------------------------------

# Put sensor into "standard ranging" mode
write(0x00, 0x01)       # Fresh boot
time.sleep(0.005)

# Set continuous ranging mode
write(0x80, 0x01)
write(0xFF, 0x01)
write(0x00, 0x00)
write(0x91, read(0x91))  # uses stored calibration
write(0x00, 0x01)
write(0xFF, 0x00)
write(0x80, 0x00)

write(0x00, 0x04)  # start continuous ranging

print("VL53L0X started. Reading distance...")

# -------------------------------------------------
# CONTINUOUS READ
# -------------------------------------------------
while True:
    d_mm = read_word(0x14)   # distance register
    print("Distance:", d_mm, "mm  |", d_mm/10, "cm")
    time.sleep(0.05)