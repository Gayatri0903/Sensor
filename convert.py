import time
import board
import busio
import adafruit_vl53l0x

class VL53L0XReader:
    def __init__(self, delay=0.1):
        self.delay = delay

        # Init I2C
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_vl53l0x.VL53L0X(i2c)

        print("VL53L0X initialized. Starting continuous readings...\n")

    def read_raw(self):
        """Return raw distance in mm."""
        return self.sensor.range

    def read_mm(self):
        return self.read_raw()

    def read_cm(self):
        return self.read_raw() / 10.0

    def stream(self):
        """Print distance continuously."""
        while True:
            raw = self.read_raw()
            mm = raw
            cm = mm / 10.0

            print(f"RAW: {raw:4d} | {mm:4d} mm | {cm:6.2f} cm")

            time.sleep(self.delay)


# ---------------------
# RUN DIRECTLY FROM FILE
# ---------------------
if __name__ == "__main__":
    sensor = VL53L0XReader(delay=0.1)
    sensor.stream()
