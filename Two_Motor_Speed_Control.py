import RPi.GPIO as GPIO
import time

# GPIO pins for Motor 1
M1_DIR = 17
M1_PWM = 18  # hardware PWM recommended

# GPIO pins for Motor 2
M2_DIR = 22
M2_PWM = 23

GPIO.setmode(GPIO.BCM)

GPIO.setup(M1_DIR, GPIO.OUT)
GPIO.setup(M1_PWM, GPIO.OUT)
GPIO.setup(M2_DIR, GPIO.OUT)
GPIO.setup(M2_PWM, GPIO.OUT)

# Create PWM objects (1000 Hz)
pwm1 = GPIO.PWM(M1_PWM, 1000)
pwm2 = GPIO.PWM(M2_PWM, 1000)

pwm1.start(0)
pwm2.start(0)

def motors(direction, speed):
    # direction: 1 = forward, 0 = reverse
    # speed: 0–100 %
    GPIO.output(M1_DIR, direction)
    GPIO.output(M2_DIR, direction)

    pwm1.ChangeDutyCycle(speed)
    pwm2.ChangeDutyCycle(speed)

try:
    print("Forward HIGH SPEED for 1 minute...")
    motors(1, 100)      # Forward full speed
    time.sleep(60)

    print("Stop for 3 seconds...")
    motors(1, 0)
    time.sleep(3)

    print("Reverse HIGH SPEED for 1 minute...")
    motors(0, 100)      # Reverse full speed
    time.sleep(60)

    print("Stop.")
    motors(1, 0)

except KeyboardInterrupt:
    pass

pwm1.stop()
pwm2.stop()
GPIO.cleanup()