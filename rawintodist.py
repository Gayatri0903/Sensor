#!/usr/bin/python3
from smbus2 import SMBus
import time

I2C_ADDR = 0x29
bus = SMBus(1)

# -----------------------------
# Basic Register Helpers
# -----------------------------
def write_reg(reg, val):
    bus.write_byte_data(I2C_ADDR, reg, val)

def read_reg(reg):
    return bus.read_byte_data(I2C_ADDR, reg)

def read_word(reg):
    high = read_reg(reg)
    low  = read_reg(reg + 1)
    return (high << 8) | low

# -----------------------------
# Start Single Shot Measurement
# -----------------------------
def start_measurement():
    write_reg(0x00, 0x01)  # SYSRANGE_START → 1 = start single shot

# -----------------------------
# Wait For Measurement Ready
# -----------------------------
def wait_for_ready():
    while True:
        status = read_reg(0x13)  # RESULT_INTERRUPT_STATUS
        if status & 0x07:        # New Sample Ready
            break
        time.sleep(0.005)

# -----------------------------
# Read Raw Measurement Block
# -----------------------------
def read_raw_distance():
    # 0x14 = RESULT_RANGE_STATUS
    # 0x1E = distance (high byte)
    # 0x1F = distance (low byte)
    distance = read_word(0x1E)
    return distance

# -----------------------------
# Clear interrupt
# -----------------------------
def clear_interrupt():
    write_reg(0x0B, 0x01)

# -----------------------------
# Main Loop
# -----------------------------
print("Reading VL53L0X raw distance...\n")

while True:
    start_measurement()
    wait_for_ready()

    raw_mm = read_raw_distance()

    if raw_mm == 0:
        print("⚠ Invalid / No target detected")
    else:
        print("Distance:", raw_mm, "mm")

    clear_interrupt()
    time.sleep(0.1)