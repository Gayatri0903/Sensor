import RPi.GPIO as GPIO
import time

# -----------------------------
# GPIO PIN SETUP
# -----------------------------
M1_DIR = 17
M1_PWM = 18   # hardware PWM pin on Raspberry Pi

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

# Global speed (0–100)
speed_percent = 100


# -----------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------

def set_speed(percent):
    """
    Set speed for both motors (0–100%).
    """
    global speed_percent
    speed_percent = max(0, min(100, percent))


def apply_pwm():
    """
    Apply the PWM duty cycle to both motors.
    """
    pwm1.ChangeDutyCycle(speed_percent)
    pwm2.ChangeDutyCycle(speed_percent)


def stop(seconds=0):
    """
    Stop both motors (0 duty cycle).
    """
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)

    if seconds > 0:
        time.sleep(seconds)


def run_forward(seconds):
    """
    Run both motors forward for X seconds.
    """
    GPIO.output(M1_DIR, GPIO.HIGH)
    GPIO.output(M2_DIR, GPIO.HIGH)

    apply_pwm()
    time.sleep(seconds)


def run_reverse(seconds):
    """
    Run both motors backward for X seconds.
    """
    GPIO.output(M1_DIR, GPIO.LOW)
    GPIO.output(M2_DIR, GPIO.LOW)

    apply_pwm()
    time.sleep(seconds)


# -----------------------------------------------------
# MAIN SEQUENCE
# -----------------------------------------------------
try:
    set_speed(100)  # High speed

    run_forward(60)  # run forward 1 minute
    stop(3)

    run_reverse(60)  # run backward 1 minute
    stop(3)

    print("Cycle done.")

except KeyboardInterrupt:
    pass

finally:
    stop()
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()