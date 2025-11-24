from smbus2 import SMBus

bus = SMBus(1)              # I2C bus 1
address = 0x29              # I2C device address
register = 0x01             # Register address
data = 0x20                 # Data to write

bus.write_byte_data(address, register, data)
print("Done!")