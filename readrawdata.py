from smbus2 import SMBus
import time
from collections import deque

# ---- USER SETTINGS ----
I2C_ADDRESS = 0x29
REG_MSB = 0x14
REG_LSB = 0x15
# If you know sensor SCALE and OFFSET, set them here (SCALE in mm per raw count)
SCALE = None     # e.g. 0.1  -> raw*0.1 = mm; set to None to auto-calibrate
OFFSET = 0.0
BUF_LEN = 5
# ------------------------

bus = SMBus(1)
buf = deque(maxlen=BUF_LEN)

def read_raw():
    msb = bus.read_byte_data(I2C_ADDRESS, REG_MSB)
    lsb = bus.read_byte_data(I2C_ADDRESS, REG_LSB)
    raw = (msb << 8) | lsb
    # if signed:
    # if raw & 0x8000: raw -= (1<<16)
    return raw

def calibrate_two_point(r1, d1_mm, r2, d2_mm):
    if r2 == r1:
        raise ValueError("r1 and r2 must differ")
    scale = (d2_mm - d1_mm) / (r2 - r1)
    offset = d1_mm - scale * r1
    return scale, offset

def smooth(val):
    buf.append(val)
    return sum(buf) / len(buf)

# Optional: run calibration if SCALE is None
if SCALE is None:
    # Example: the user must supply two raw readings at known distances.
    # Replace these placeholders with actual measurements you record.
    print("Auto-calibration required. Measure raw at two known distances.")
    r1 = int(input("Raw at distance d1 (mm), enter raw1: "))
    d1 = float(input("Enter known distance d1 (mm): "))
    r2 = int(input("Raw at distance d2 (mm), enter raw2: "))
    d2 = float(input("Enter known distance d2 (mm): "))
    SCALE, OFFSET = calibrate_two_point(r1, d1, r2, d2)
    print(f"Calibration done. SCALE={SCALE}, OFFSET={OFFSET}")

print("Reading (CTRL+C to stop)...")
try:
    while True:
        raw = read_raw()
        distance = raw * SCALE + OFFSET   # mm
        distance_smooth = smooth(distance)
        print(f"RAW={raw:5d}  DIST(mm)={distance:7.2f}  SMOOTH(mm)={distance_smooth:7.2f}")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopped.")