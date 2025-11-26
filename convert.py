import time
import board
import busio
import adafruit_vl53l0x

class VL53L0XReader:
    def __init__(self, scl=board.SCL, sda=board.SDA, delay=0.1):
        """
        VL53L0X continuous distance reader.

        :param scl: SCL pin (default: board.SCL)
        :param sda: SDA pin (default: board.SDA)
        :param delay: Delay between readings in seconds (default: 0.1)
        """
        self.delay = delay
        
        # Initialize I2C bus
        self.i2c = busio.I2C(scl, sda)

        # Initialize sensor
        self.sensor = adafruit_vl53l0x.VL53L0X(self.i2c)

        print("VL53L0X initialized. Starting continuous reading...")

    def read_raw(self):
        """
        Reads raw sensor range data (in millimeters).
        The Adafruit driver already gives raw distance.
        """
        return self.sensor.range

    def read_distance_mm(self):
        """
        Converts raw data to distance in millimeters (same as raw).
        """
        raw = self.read_raw()
        return raw  # already mm

    def read_distance_cm(self):
        """
        Converts raw distance into centimeters.
        """
        return self.read_distance_mm() / 10.0

    def start_continuous(self):
        """
        Continuously read raw + converted distance.
        """
        while True:
            raw = self.read_raw()
            dist_mm = raw
            dist_cm = dist_mm / 10.0

            print(f"Raw: {raw}  |  Distance: {dist_mm} mm  |  {dist_cm:.2f} cm")
            time.sleep(self.delay)
