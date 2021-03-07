import RPi.GPIO as GPIO
import time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# SENSOR PIN = 13
#GPIO.setup(SENSOR_PIN, GPIO.IN)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
pwm=GPIO.PWM(29, 50)
pwm.start(0)


def setAngle(angle):
    duty = angle / 18 + 3
    GPIO.output(29, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(29, False)
    pwm.ChangeDutyCycle(duty)

def main():
    GPIO.setup(21, GPIO.HIGH)
    setAngle(0)
    time.sleep(2)
    setAngle(180)
    GPIO.setup(21, GPIO.LOW)
    time.sleep(2)
    pwm.stop()
     
    # def my_callback(channel):
    #     # Here, alternatively, an application / command etc. can be started.
    #     print('There was a movement!')
    #  
    # try:
    #     GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=my_callback)
    #     while True:
    #         time.sleep(100)
    # except KeyboardInterrupt:
    #     print("Finish...")
    GPIO.cleanup()

    return 0;

main()
