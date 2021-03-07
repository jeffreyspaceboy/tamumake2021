import digitalio

import busio
import adafruit_amg88xx

import board

print("STATUS: Starting Up!")

# Try to great a Digital input
# pin = digitalio.DigitalInOut(board.D4)
# print("Digital IO ok!")

# Try to create an I2C device
# i2c = busio.I2C(board.SCL, board.SDA)
# print("I2C ok!")

# Try to create an SPI device
# spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
# print("SPI ok!")

i2c_bus = busio.I2C(board.SCL, board.SDA)

amg = adafruit_amg88xx.AMG88XX(i2c_bus)

print(amg.pixels)


print("STATUS: All Done!")
