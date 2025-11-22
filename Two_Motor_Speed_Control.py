import RPi.GPIO as GPIO
import time

#pin setup
motorA_in1 = 17
motorA_in2 = 18
motorB_in1 = 22
motorB_in2 = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(motorA_in1, GPIO.OUT)
GPIO.setup(motorA_in2, GPIO.OUT)    
GPIO.setup(motorB_in1, GPIO.OUT)
GPIO.setup(motorB_in2, GPIO.OUT)

def motorA_forward();
    GPIO.output(motorA_in1, GPIO.HIGH)
    GPIO.output(motorA_in2, GPIO.LOW)

def motorA_backward():
    GPIO.output(motorA_in1, GPIO.LOW)
    GPIO.output(motorA_in2, GPIO.HIGH)

def motorB_forward():
    GPIO.output(motorA_in1, GPIO.HIGH)
    GPIO.output(motorA_in2, GPIO.LOW)   

def motorB_backward():
    GPIO.output(motorB_in1, GPIO.LOW)
    GPIO.output(motorB_in2, GPIO.HIGH)

def motors_stop():
    GPIO.output(motorA_in1, GPIO.LOW)
    GPIO.output(motorA_in2, GPIO.LOW)
    GPIO.output(motorB_in1, GPIO.LOW)
    GPIO.output(motorB_in2, GPIO.LOW)

#Run Motors
print("Motors Forward")
motorA_forward()
motorB_forward()
time.sleep(2)

print("Motors Backward")
motorA_backward()   
motorB_backward()
time.sleep(2)

print("Motors Stop")
motors_stop()

GPIO.cleanup()