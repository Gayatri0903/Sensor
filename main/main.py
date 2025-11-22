# main.py
from sensor import DistanceSensor
from motors import Motors
import time

try:
    motors = Motors()
    sensor = DistanceSensor()

    print("System Started\n")

    # -------------------------
    # Run FORWARD for 1 minute
    # -------------------------
    print("Motors Forward...")
    motors.forward(100)
    start_time = time.time()

    while time.time() - start_time < 60:
        d = sensor.read_cm()
        print(f"Distance: {d:.1f} cm")
        time.sleep(0.1)

    motors.stop()
    time.sleep(2)

    # -------------------------
    # Run REVERSE for 1 minute
    # -------------------------
    print("\nMotors Reverse...")
    motors.reverse(100)
    start_time = time.time()

    while time.time() - start_time < 60:
        d = sensor.read_cm()
        print(f"Distance: {d:.1f} cm")
        time.sleep(0.1)

    motors.stop()
    print("\nDone.")

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    motors.cleanup()
    sensor.stop()
    print("GPIO cleaned up.")