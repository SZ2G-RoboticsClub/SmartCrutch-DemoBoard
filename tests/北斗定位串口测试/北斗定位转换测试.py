from machine import UART
from mpython import *
import time

uart1 = machine.UART(1, baudrate=9600, tx=Pin.P14, rx=Pin.P13)

i = 0
lat = 0
lon = 0
while True:
    if uart1.any() and i == 0:
        time.sleep(0.1)
        loc_get = uart1.readline()
        if 'GNGLL' in loc_get:
            print(loc_get)
            i = i + 1
            location = (str(loc_get).split(','))
            if location[2] == 'N':
                lat = float(location[1])
            elif location[2] == 'S':
                lat = float(location[1]) * -1
            else:
                lat = 0
            if location[4] == 'E':
                lon = float(location[3])
            elif location[4] == 'W':
                lon = float(location[3]) * -1
            else:
                lon = 0

            print(location)
            print(lat)
            print(lon)
