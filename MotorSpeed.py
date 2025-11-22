import RPi.GPIO as GPIO
import time

# Motor 1 pins
M1_DIR = 17
M1_PWM = 18     # hardware PWM

# Motor 2 pins
M2_DIR = 22
M2_PWM = 23

GPIO.setmode(GPIO.BCM)

GPIO.setup(M1_DIR, GPIO.OUT)
GPIO.setup(M1_PWM, GPIO.OUT)

GPIO.setup(M2_DIR, GPIO.OUT)
GPIO.setup(M2_PWM, GPIO.OUT)

# PWM created at 1000 Hz (recommended for MD10C R3)
pwm1 = GPIO.PWM(M1_PWM, 1000)
pwm2 = GPIO.PWM(M2_PWM, 1000)

pwm1.start(0)
pwm2.start(0)

# SPEED = 100 (High speed)
SPEED = 100

def motors_forward():
    GPIO.output(M1_DIR, 1)
    GPIO.output(M2_DIR, 1)
    pwm1.ChangeDutyCycle(SPEED)
    pwm2.ChangeDutyCycle(SPEED)

def motors_reverse():
    GPIO.output(M1_DIR, 0)
    GPIO.output(M2_DIR, 0)
    pwm1.ChangeDutyCycle(SPEED)
    pwm2.ChangeDutyCycle(SPEED)

def motors_stop():
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)

try:
    while True:
        print("Forward  (HIGH SPEED)")
        motors_forward()
        time.sleep(6)

        print("Stop 3 sec")
        motors_stop()
        time.sleep(3)

        print("Reverse  (HIGH SPEED)")
        motors_reverse()
        time.sleep(6)

        print("Stop 3 sec")
        motors_stop()
        time.sleep(3)

except KeyboardInterrupt:
    pass

motors_stop()
pwm1.stop()
pwm2.stop()
GPIO.cleanup()