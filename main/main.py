# main.py
from sensor import DistanceSensor
from motors import Motors
import time

# Motor pins
M1_DIR = 23
M1_PWM = 24
M2_DIR = 27
M2_PWM = 22

motors = Motors(M1_DIR, M1_PWM, M2_DIR, M2_PWM)
sensor = DistanceSensor()

print("System Started")

try:
    print("Motors Forward for 1 minute...")
    motors.forward(100)

    start = time.time()
    while time.time() - start < 60:
        dist = sensor.read_distance()
        print(f"Distance: {dist} cm")
        time.sleep(0.2)

    print("Motors Reverse for 1 minute...")
    motors.reverse(100)

    start = time.time()
    while time.time() - start < 60:
        dist = sensor.read_distance()
        print(f"Distance: {dist} cm")
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    motors.cleanup()
    print("GPIO cleaned up.")