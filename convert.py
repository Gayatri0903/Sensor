import time
import board
import busio
import adafruit_vl53l0x

class VL53L0XContinuous:
    """
    Read raw VL53L0X data continuously using Adafruit driver internal continuous mode.
    """

    def __init__(self, delay=0.05):
        self.delay = delay

        # Create I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)

        # Create device object
        self.sensor = adafruit_vl53l0x.VL53L0X(i2c)

        # Enable low-level continuous mode (from internal driver)
        self.sensor.start_continuous()
        time.sleep(0.05)

        print("VL53L0X continuous mode started.")

    def read_raw(self):
        """
        Read raw ranging data from internal register.
        In continuous mode, .range returns raw mm distance WITHOUT triggering a new measurement.
        """
        return self.sensor.range  # already raw mm from the device

    def read_mm(self):
        """
        Distance in millimeters.
        """
        return self.read_raw()

    def read_cm(self):
        """
        Distance in centimeters.
        """
        return self.read_raw() / 10.0

    def stream(self):
        """
        Continuously output raw data + converted distance.
        """
        try:
            while True:
                raw = self.read_raw()
                mm = raw
                cm = raw / 10.0

                print(f"RAW: {raw:4d} | {mm:4d} mm | {cm:6.2f} cm")

                time.sleep(self.delay)

        except KeyboardInterrupt:
            print("Stopping continuous mode...")
            self.sensor.stop_continuous()
            print("Stopped.")

