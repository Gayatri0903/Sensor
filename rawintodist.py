from smbus2 import SMBus
import time

I2C_BUS = 1
ADDR = 0x29

# Result registers for VL53L0X-compatible sensors
RESULT_RANGE_STATUS = 0x14
RESULT_DISTANCE_HIGH = 0x1E
RESULT_DISTANCE_LOW = 0x1F

def read_distance():
    with SMBus(I2C_BUS) as bus:
        # Read two bytes of distance
        high = bus.read_byte_data(ADDR, RESULT_DISTANCE_HIGH)
        low  = bus.read_byte_data(ADDR, RESULT_DISTANCE_LOW)

        distance = (high << 8) | low  # mm
        return distance

if __name__ == "__main__":
    print("Reading distance...")

    while True:
        try:
            dist = read_distance()
            print("Distance:", dist, "mm")
        except Exception as e:
            print("I2C Error:", e)

        time.sleep(0.2)