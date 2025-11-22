# sensor.py
from vl53l1x import vl53l1x

class DistanceSensor:
    def __init__(self):
        self.sensor = VL53L1X(i2c_bus=1, i2c_address=0x29)
        self.sensor.open()
        self.sensor.start_ranging()

    def read_cm(self):
        dist_mm = self.sensor.get_distance()
        return dist_mm / 10.0   # convert mm → cm

    def stop(self):
        self.sensor.stop_ranging()