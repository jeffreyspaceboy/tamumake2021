import os
import math
import time

import numpy as np
import pygame
import busio
import board
import pwmio

from scipy.interpolate import griddata

from colour import Color

import adafruit_amg88xx



servo = pwmio.PWMOut(board.D5, frequency=50)

def servo_duty_cycle(pulse_ms, frequency=50):
    period_ms = 1.0 / frequency * 1000.0
    duty_cycle = int(pulse_ms / (period_ms / 65535.0))
    return duty_cycle
 

i2c_bus = busio.I2C(board.SCL, board.SDA)


MINTEMP = 26.0 # low range of the sensor (this will be blue on the screen)
MAXTEMP = 32.0 # high range of the sensor (this will be red on the screen)

COLORDEPTH = 1024 # how many color values we can have

os.putenv("SDL_FBDEV", "/dev/fb1")
pygame.init()

sensor = adafruit_amg88xx.AMG88XX(i2c_bus) # initialize the sensor

points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]


height = 500 # sensor is an 8x8 grid so lets do a square
width = 500


blue = Color("indigo") # the list of colors we can choose from
colors = list(blue.range_to(Color("red"), COLORDEPTH))

colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors] # create the array of colors

displayPixelWidth = width / 30
displayPixelHeight = height / 30

lcd = pygame.display.set_mode((width, height))
lcd.fill((255, 0, 0))

pygame.display.update()
pygame.mouse.set_visible(False)

lcd.fill((0, 0, 0))
pygame.display.update()


def constrain(val, min_val, max_val): # some utility functions
    return min(max_val, max(min_val, val))

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

time.sleep(0.1) # let the sensor initialize

while True:
    pixels = [] # read the pixels
    for row in sensor.pixels:
        pixels = pixels + row
    pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]
    bicubic = griddata(points, pixels, (grid_x, grid_y), method="cubic") # perform interpolation
    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH - 1)],(
                    displayPixelHeight * ix,
                    displayPixelWidth * jx,
                    displayPixelHeight,
                    displayPixelWidth,
                ),
            )
    pygame.display.update()
