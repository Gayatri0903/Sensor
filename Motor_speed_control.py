import RPi.GPIO as GPIO
import time

#pin definition
PWM_PIN = 18
DIR_PIN = 23 

#setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)

# MD10C R3 supports PWM 
pwm = GPIO.PWM(PWM_PIN, 10000)
pwm.start(0) #initially motor is off

def set_motor(speed):

    #Set motor speed using MD10C R3
    #Speed Range: -100 to +100
    #positive - forward
    #negative - reserve
     
     #direction control
     if speed >=0:
          GPIO.output(DIR_PIN, GPIO.HIGH)
     else:
            GPIO.output(DIR_PIN,GPIO.LOW)

    ##speed control
     duty = max(0, min(100, abs(speed)))
     pwm.ChangeDutyCycle(duty)
     
     
     
     
     
try :
        while True:
            print("Forward at 30%")
            set_motor(20)
            time.sleep(2)

            print("Forward at 80%")
            set_motor(80)
            time.sleep(2)
            
            print("Forward at 40%")
            set_motor(80)
            time.sleep(2)


            print("Stop")
            set_motor(80)
            time.sleep(2)

except KeyboardInterrupt:
    pass

pwm.stop()
GPIO.cleanup()

      

