from vl53l1x import VL53L1X

import time

class DistanceSensor:
    def __init__(self):
        self.sensor = VL53L1X()
        self.sensor.init()
        print("VL53L1X Sensor Ready")

    def read_cm(self):
        data = self.sensor.get_ranging_data()
        dist_mm = data.distance_mm[0]  # zone 0
        return dist_mm / 10.0          # mm → cm

    def stop(self):
        pass   # nothing to stop for this sensor
