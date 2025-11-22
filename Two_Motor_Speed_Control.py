import RPi.GPIO as GPIO
import time

# MOTOR 1 (MD10C #1)
M1_DIR = 17
M1_PWM = 18    # hardware PWM pin

# MOTOR 2 (MD10C #2)
M2_DIR = 22
M2_PWM = 23

GPIO.setmode(GPIO.BCM)

# Set all pins low initially for safety
GPIO.setup(M1_DIR, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(M1_PWM, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(M2_DIR, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(M2_PWM, GPIO.OUT, initial=GPIO.LOW)

# Create PWM objects at 1kHz
pwm1 = GPIO.PWM(M1_PWM, 1000)
pwm2 = GPIO.PWM(M2_PWM, 1000)

# Start PWM at 0% (motors OFF first)
pwm1.start(0)
pwm2.start(0)

try:
    print("Motors running at high speed...")

    # Set direction: 1 = forward, 0 = reverse
    GPIO.output(M1_DIR, GPIO.HIGH)
    GPIO.output(M2_DIR, GPIO.HIGH)

    # High speed (90–100%). 90% is safer than full 100%.
    pwm1.ChangeDutyCycle(95)
    pwm2.ChangeDutyCycle(95)

    time.sleep(5)  # run for 5 seconds

    print("Stopping motors...")
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)

finally:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()