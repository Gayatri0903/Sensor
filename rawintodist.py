#!/usr/bin/python3
import smbus2
import time

I2C_ADDR = 0x29
bus = smbus2.SMBus(1)

# ---- BASIC REGISTER READ/WRITE ----
def write_reg(reg, val):
    bus.write_byte_data(I2C_ADDR, reg, val)

def read_reg(reg):
    return bus.read_byte_data(I2C_ADDR, reg)

def read_word(reg):
    high = read_reg(reg)
    low  = read_reg(reg + 1)
    return (high << 8) | low

# ---- START CONTINUOUS RANGING ----
def start_continuous():
    write_reg(0x80, 0x01)
    write_reg(0xFF, 0x01)
    write_reg(0x00, 0x00)

    write_reg(0x91, 0x3C)   # default static value for VL53L0X
    write_reg(0x00, 0x01)

    write_reg(0xFF, 0x00)
    write_reg(0x80, 0x00)

    write_reg(0x00, 0x04)   # continuous mode

# ---- READ RAW & DISTANCE ----
def read_measurement():
    status = read_reg(0x13)      # RESULT_INTERRUPT_STATUS
    
    if (status & 0x07) == 0:     # no new data
        return None

    # RAW peak signal (16-bit)
    raw_signal = read_word(0xB6)

    # RAW ambient (16-bit)
    raw_ambient = read_word(0xBC)

    # DISTANCE (16-bit, mm)
    dist = read_word(0x14)

    # clear interrupt
    write_reg(0x0B, 0x01)

    return raw_signal, raw_ambient, dist


# --------------- MAIN LOOP ------------------
start_continuous()
print("Reading distance + raw data…")

while True:
    data = read_measurement()

    if data is None:
        print("Waiting…")
        time.sleep(0.03)
        continue

    raw_signal, raw_ambient, dist = data

    print(f"Distance: {dist} mm | Raw Signal: {raw_signal} | Raw Ambient: {raw_ambient}")
    time.sleep(0.05)
