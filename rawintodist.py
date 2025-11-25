import smbus
import time

bus = smbus.SMBus(1)
ADDR = 0x29

REG_DIST_L = 0x14
REG_DIST_H = 0x15
REG_STATUS = 0x16

while True:
    try:
        dist_l = bus.read_byte_data(ADDR, REG_DIST_L)
        dist_h = bus.read_byte_data(ADDR, REG_DIST_H)
        status = bus.read_byte_data(ADDR, REG_STATUS)

        distance = (dist_h << 8) | dist_l

        if status != 0:       # 0 = OK (from your dump)
            print("Invalid / no target detected")
        else:
            print("Distance:", distance, "mm")

    except Exception as e:
        print("Error:", e)

    time.sleep(0.1)