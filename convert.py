import time
import board
import busio
import adafruit_vl53l0x

class VL53L0XReader:
    def __init__(self, delay=0.1):
        self.delay = delay
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_vl53l0x.VL53L0X(i2c)
        print("VL53L0X initialized.")

    def read_raw(self):
        """Raw range reading in millimeters."""
        return self.sensor.range

    def read_mm(self):
        return self.read_raw()

    def read_cm(self):
        return self.read_raw() / 10.0

    def stream(self):
        print("Starting continuous readings...")
        while True:
            raw = self.read_raw()
            mm = raw
            cm = raw / 10.0

            print(f"RAW: {raw:4d} | {mm:4d} mm | {cm:6.2f} cm")

            time.sleep(self.delay)
