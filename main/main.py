from sensor import DistanceSensor
from motors import Motors
import time
import RPi.GPIO as GPIO

# Motor pins (BCM)
M1_IN = 17
M1_PWM = 18
M2_IN = 22
M2_PWM = 23

# HC-SR04 Pins
TRIG = 24
ECHO = 25

sensor = DistanceSensor(TRIG, ECHO)
motors = Motors(M1_IN, M1_PWM, M2_IN, M2_PWM)

try:
    while True:
        dist = sensor.read_cm()
        print("Distance:", dist, "cm")

        if dist < 20:
            print("Obstacle detected! Moving backward.")
            motors.backward(100)
            time.sleep(1)
            motors.stop()
            time.sleep(1)
        else:
            print("Path clear → Moving forward")
            motors.forward(100)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped.")
    motors.cleanup()
    GPIO.cleanup()