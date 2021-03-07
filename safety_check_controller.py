import sys
import time
import board
import busio
import adafruit_amg88xx
import RPi.GPIO as GPIO

output = False

GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)
GPIO.setup(27,GPIO.IN)

def thermal_camera(threshold):
    i2c = busio.I2C(board.SCL, board.SDA)
    amg = adafruit_amg88xx.AMG88XX(i2c)
    max_temp = 0.0
    time.sleep(1)
    for row in amg.pixels:
        for temp in row:
            if(temp > max_temp):
                max_temp = temp
    print(max_temp)
    if(max_temp >= threshold):
        return(1)
    else:
        return(0)

def motion_sensor():
    return(GPIO.input(27))

def main():
    MOTION_TIME = 3
    THERMAL_TIME = 3
    TEMP_THRESH = 30
    is_hot = True;
    has_motion = True;
    time_cool = 0;
    time_hot = 0;
    time_away = 0;
    
    t_time = 0;
    m_time = 0;
    while(True):
        if(motion_sensor() == 1):
            has_motion = True
            m_time = 0
            time_away = 0
        elif(m_time > MOTION_TIME and motion_sensor() == 0):
            has_motion = False
            time_away += 1
        print(has_motion)
        
        if(thermal_camera(TEMP_THRESH) == 1):
            is_hot = True
            t_time = 0
            time_cool = 0
            time_hot += 1
        elif(t_time > THERMAL_TIME and thermal_camera(TEMP_THRESH) == 0):
            is_hot = False
            time_hot = 0
        
        m_time += 1;
        t_time += 1;
        time_cool += 1;
        if(time_hot >= 10 and time_away >= 10):
            output = True
        else:
            output = False
        if((not is_hot) and (time_cool >= 10)):
            output False
            break;
    return(0)
            
main()
    
    