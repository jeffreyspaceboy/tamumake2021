import sys
import time
import busio
import board
import adafruit_amg88xx

i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

time.sleep(1)

def main(threshold):
    max_temp = 0.0
    for row in amg.pixels:
        for temp in row:
            if(temp > max_temp):
                max_temp = temp
    print(max_temp)
    if(max_temp >= threshold):
        return(1)
    else:
        return(0)

if __name__ =='__main__' :
    code = main(float(sys.argv[1]))