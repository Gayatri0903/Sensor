import time
import board
import busio
import adafruit_vl53l0x
import RPi.GPIO as GPIO

# ================================
# MOTOR DRIVER CLASS (MD10C R3)
# ================================
class Motor:
    def __init__(self, pwm_pin, dir_pin, freq=1000):
        GPIO.setup(pwm_pin, GPIO.OUT)
        GPIO.setup(dir_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(pwm_pin, freq)
        self.dir = dir_pin

        self.pwm.start(0)

    def set_speed(self, speed):
        """
        speed = -100 to +100
        negative = reverse
        """
        if speed < 0:
            GPIO.output(self.dir, GPIO.LOW)
            speed = -speed
        else:
            GPIO.output(self.dir, GPIO.HIGH)

        if speed > 100:
            speed = 100

        self.pwm.ChangeDutyCycle(speed)

    def stop(self):
        self.pwm.ChangeDutyCycle(0)


# ================================
# SENSOR CLASS
# ================================
class VL53L0XReader:
    def __init__(self, delay=0.1):
        self.delay = delay

        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_vl53l0x.VL53L0X(i2c)

        print("VL53L0X Initialized.")

    def read_mm(self):
        return self.sensor.range

    def read_cm(self):
        return self.sensor.range / 10.0


# ================================
# MAIN CONTROL LOGIC
# ================================
GPIO.setmode(GPIO.BCM)

# Motor A pins
M1_PWM = 18
M1_DIR = 23

# Motor B pins
M2_PWM = 19
M2_DIR = 24

motor1 = Motor(M1_PWM, M1_DIR)
motor2 = Motor(M2_PWM, M2_DIR)

sensor = VL53L0XReader(delay=0.1)

print("Starting robot control...\n")

try:
    while True:
        dist = sensor.read_cm()

        print(f"Distance: {dist:.2f} cm")

        # ===============================
        # SPEED LOGIC BASED ON DISTANCE
        # ===============================
        if dist > 80:
            # FAR → HIGH SPEED
            motor_speed = 90
            print("High speed")

        elif 40 < dist <= 80:
            # MEDIUM RANGE → MEDIUM SPEED
            motor_speed = 60
            print("Medium speed")

        elif 20 < dist <= 40:
            # CLOSE → LOW SPEED
            motor_speed = 30
            print("Low speed")

        else:
            # TOO CLOSE → STOP
            motor1.stop()
            motor2.stop()
            print("STOP (Obstacle too close)")
            time.sleep(0.1)
            continue

        # Apply speed to both motors (forward)
        motor1.set_speed(motor_speed)
        motor2.set_speed(motor_speed)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopping...")
    motor1.stop()
    motor2.stop()
    GPIO.cleanup()
