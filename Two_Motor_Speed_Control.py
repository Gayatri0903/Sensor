import pigpio
import time

pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("pigpiod not running")

M1_DIR = 17
M1_PWM = 18
M2_DIR = 22
M2_PWM = 23

# Setup direction pins as outputs, set low initially
pi.set_mode(M1_DIR, pigpio.OUTPUT)
pi.set_mode(M2_DIR, pigpio.OUTPUT)
pi.write(M1_DIR, 0)
pi.write(M2_DIR, 0)

# Set PWM frequency (hardware supports per-pin)
pi.set_PWM_frequency(M1_PWM, 1000)
pi.set_PWM_frequency(M2_PWM, 1000)

# Set both directions same
pi.write(M1_DIR, 1)
pi.write(M2_DIR, 1)

# pigpio uses 0-255 duty range
duty = int(0.95 * 255)  # 95% duty
pi.set_PWM_dutycycle(M1_PWM, duty)
pi.set_PWM_dutycycle(M2_PWM, duty)

time.sleep(5)

# Stop both
pi.set_PWM_dutycycle(M1_PWM, 0)
pi.set_PWM_dutycycle(M2_PWM, 0)

pi.stop()