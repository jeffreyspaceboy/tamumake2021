import os
import sys
import math
import time

import numpy as np
import pygame
import busio
import board

from scipy.interpolate import griddata
from colour import Color
import adafruit_amg88xx

i2c_bus = busio.I2C(board.SCL, board.SDA)

MINTEMP = 26.0
MAXTEMP = 40.0

COLORDEPTH = 1024

os.putenv("SDL_FBDEV", "/dev/fb1")
pygame.init()

sensor = adafruit_amg88xx.AMG88XX(i2c_bus)
points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

height = 500
width = 500

blue = Color("indigo")
colors = list(blue.range_to(Color("red"), COLORDEPTH))
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

displayPixelWidth = width / 30
displayPixelHeight = height / 30

lcd = pygame.display.set_mode((width, height))
lcd.fill((255, 0, 0))

pygame.display.update()
pygame.mouse.set_visible(False)

lcd.fill((0, 0, 0))
pygame.display.update()

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

time.sleep(0.1)
def main(threshold):
    max_temp = 0.0
    pixels = []
    for row in sensor.pixels:
        for temp in row:
            if(temp > max_temp):
                max_temp = temp
            #print(['{0:.1f}'.format(temp) for temp in row])
            #print("")
        pixels = pixels + row
    pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]
    bicubic = griddata(points, pixels, (grid_x, grid_y), method="cubic")
    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            pygame.draw.rect(lcd,colors[constrain(int(pixel), 0, COLORDEPTH - 1)],(
                    displayPixelHeight * ix,
                    displayPixelWidth * jx,
                    displayPixelHeight,
                    displayPixelWidth,
                ),
            )
    pygame.display.update()
    print(max_temp)
    if(max_temp >= threshold):
        return(True)
    else:
        return(False)

main(float(sys.argv[1]))