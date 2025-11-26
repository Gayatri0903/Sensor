import time
import board
import busio
import adafruit_vl53l0x
import lgpio

# ======================================
# MOTOR DRIVER (MD10C R3) – Pi 5 Version
# ======================================
class Motor:
    def __init__(self, chip, pwm_pin, dir_pin, freq=1000):
        self.chip = chip
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.freq = freq

        # Claim pins
        lgpio.gpio_claim_output(chip, dir_pin)
        lgpio.gpio_claim_output(chip, pwm_pin)

        # Set PWM output (0% duty at start)
        lgpio.tx_pwm(chip, pwm_pin, freq, 0)

    def set_speed(self, speed):
        """
        speed: -100 to +100
        - = reverse
        + = forward
        """
        direction = 1 if speed >= 0 else 0
        speed = abs(speed)

        if speed > 100:
            speed = 100

        # Set direction
        lgpio.gpio_write(self.chip, self.dir_pin, direction)

        # Set duty cycle
        lgpio.tx_pwm(self.chip, self.pwm_pin, self.freq, speed)

    def stop(self):
        lgpio.tx_pwm(self.chip, self.pwm_pin, self.freq, 0)


# =====================================
# VL53L0X SENSOR READER
# =====================================
class VL53L0XReader:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_vl53l0x.VL53L0X(i2c)
        print("VL53L0X sensor initialized.")

    def distance_cm(self):
        return self.sensor.range / 10.0


# =====================================
# MAIN ROBOT LOGIC
# =====================================
def main():
    chip = lgpio.gpiochip_open(0)

    # Motor pin assignments
    M1_PWM = 18   # left motor
    M1_DIR = 23
    M2_PWM = 19   # right motor
    M2_DIR = 24

    motor1 = Motor(chip, M1_PWM, M1_DIR)
    motor2 = Motor(chip, M2_PWM, M2_DIR)

    sensor = VL53L0XReader()

    print("\nRobot Started. Press CTRL+C to stop.\n")

    try:
        while True:
            dist = sensor.distance_cm()
            print(f"Distance: {dist:.1f} cm")

            # ============================
            # SPEED CONTROL LOGIC
            # ============================
            if dist > 80:
                speed = 90
                print("➡ HIGH SPEED")

            elif 40 < dist <= 80:
                speed = 60
                print("➡ MEDIUM SPEED")

            elif 20 < dist <= 40:
                speed = 30
                print("➡ LOW SPEED")

            else:
                print("⛔ STOP — TOO CLOSE")
                motor1.stop()
                motor2.stop()
                time.sleep(0.1)
                continue

            motor1.set_speed(speed)
            motor2.set_speed(speed)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping motors...")
        motor1.stop()
        motor2.stop()
        lgpio.gpiochip_close(chip)
        print("Robot stopped.")


if __name__ == "__main__":
    main()
