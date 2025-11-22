import RPi.GPIO as GPIO
import time

# GPIO pin definitions
M1_DIR = 17  # Motor 1 Direction pin
M1_PWM = 18  # Motor 1 PWM pin

M2_DIR = 22  # Motor 2 Direction pin
M2_PWM = 23  # Motor 2 PWM pin

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)

GPIO.setup(M1_DIR, GPIO.OUT)
GPIO.setup(M1_PWM, GPIO.OUT)
GPIO.setup(M2_DIR, GPIO.OUT)
GPIO.setup(M2_PWM, GPIO.OUT)

# Setup PWM
pwm1 = GPIO.PWM(M1_PWM, 1000)  # 1 kHz frequency
pwm2 = GPIO.PWM(M2_PWM, 1000)  # 1 kHz frequency

pwm1.start(0)  # Start PWM with 0% duty cycle
pwm2.start(0)  # Start PWM with 0% duty cycle

def motor_control(direction, speed):
    GPIO.output(M1_DIR, direction)
    GPIO.output(M2_DIR, direction)

    pwm1.ChangeDutyCycle(speed)
    pwm2.ChangeDutyCycle(speed)

try:
    print("Forward")
    motor_control(1, 150)  # Forward at 75% speed
    time.sleep(5)

    print("stop")
    motor_control(1, 0)   # Stop
    time.sleep(2)
    
    print("Backward")
    motor_control(0, 150)  # Backward at 75% speed
    time.sleep(5)

    print("stop")
    motor_control(1, 0)   # Stop
    time.sleep(2)
except KeyboardInterrupt:
    pass

pwm1.stop()
pwm2.stop()
GPIO.cleanup()