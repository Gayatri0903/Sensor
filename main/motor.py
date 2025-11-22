import RPi.GPIO as GPIO
import time

class MotorControl:
    def __init__(self):
        self.M1_DIR = 17
        self.M1_PWM = 18
        self.M2_DIR = 22
        self.M2_PWM = 23

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.M1_DIR, GPIO.OUT)
        GPIO.setup(self.M1_PWM, GPIO.OUT)
        GPIO.setup(self.M2_DIR, GPIO.OUT)
        GPIO.setup(self.M2_PWM, GPIO.OUT)

        self.pwm1 = GPIO.PWM(self.M1_PWM, 1000)
        self.pwm2 = GPIO.PWM(self.M2_PWM, 1000)

        self.pwm1.start(0)
        self.pwm2.start(0)

        self.speed = 100

    def forward(self):
        GPIO.output(self.M1_DIR, GPIO.HIGH)
        GPIO.output(self.M2_DIR, GPIO.HIGH)
        self.pwm1.ChangeDutyCycle(self.speed)
        self.pwm2.ChangeDutyCycle(self.speed)
        print("Motors Forward")

    def reverse(self):
        GPIO.output(self.M1_DIR, GPIO.LOW)
        GPIO.output(self.M2_DIR, GPIO.LOW)
        self.pwm1.ChangeDutyCycle(self.speed)
        self.pwm2.ChangeDutyCycle(self.speed)
        print("Motors Reverse")

    def stop(self):
        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(0)
        print("Motors Stop")

    def run(self):
        while True:
            self.forward()
            time.sleep(5)

            self.stop()
            time.sleep(2)

            self.reverse()
            time.sleep(5)

            self.stop()
            time.sleep(2)