import smbus2
import time

bus = smbus2.SMBus(1)
addr = 0x29

# Mandatory init for VL53L0X
def init_vl53l0x():
    bus.write_byte_data(addr, 0x88, 0x00)
    bus.write_byte_data(addr, 0x80, 0x01)
    bus.write_byte_data(addr, 0xFF, 0x01)
    bus.write_byte_data(addr, 0x00, 0x00)
    bus.write_byte_data(addr, 0x91, bus.read_byte_data(addr, 0x91))
    bus.write_byte_data(addr, 0x00, 0x01)
    bus.write_byte_data(addr, 0xFF, 0x00)
    bus.write_byte_data(addr, 0x80, 0x00)

init_vl53l0x()

# Start measurement
bus.write_byte_data(addr, 0x00, 0x02)  # sysrange start continuous mode

while True:
    raw = bus.read_i2c_block_data(addr, 0x14, 14)
    print("RAW:", raw)
    time.sleep(0.1)