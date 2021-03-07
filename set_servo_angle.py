import RPi.GPIO as GPIO
import time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

SERVO_PIN = 29
def main(angle):
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    SERVO = GPIO.PWM(SERVO_PIN, 50)
    SERVO.start(0)
    duty = float(angle) / 18 + 3
    GPIO.output(SERVO_PIN, True)
    SERVO.ChangeDutyCycle(duty)
    time.sleep(1.5)
    GPIO.output(SERVO_PIN, False)
    SERVO.ChangeDutyCycle(duty)
    SERVO.stop()
    GPIO.cleanup()
    return 0;

ANGLE = sys.argv[1]
main(ANGLE)#)
