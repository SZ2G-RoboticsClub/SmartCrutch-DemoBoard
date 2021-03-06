#mPythonType:0
from mpython import *

import neopixel

my_rgb1 = neopixel.NeoPixel(Pin(Pin.P15), n=23, bpp=3, timing=1)

my_rgb2 = neopixel.NeoPixel(Pin(Pin.P13), n=23, bpp=3, timing=1)

import time

p2 = MPythonPin(2, PinMode.ANALOG)
m = 0

def common():
    global m, time_on
    oled.fill(0)
    oled.DispChar('智能云拐杖', 0, 16, 1)
    oled.DispChar('开', 0, 32, 1)
    oled.show()
    if p2.read_analog() >= 25:
        liushuideng()
    elif p2.read_analog() < 25:
        my_rgb1.brightness(20 / 100)
        my_rgb2.brightness(20 / 100)
        my_rgb1.fill( (255, 255, 255) )
        my_rgb2.fill( (255, 255, 255) )
        my_rgb1.write()
        my_rgb2.write()
    

def make_rainbow(_neopixel, _num, _bright, _offset):
    _rgb = ((255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,255,255), (0,0,255), (136,0,255), (255,0,0))
    for i in range(_num):
        t = 7 * i / _num
        t0 = int(t)
        r = round((_rgb[t0][0] + (t-t0)*(_rgb[t0+1][0]-_rgb[t0][0]))*_bright)>>8
        g = round((_rgb[t0][1] + (t-t0)*(_rgb[t0+1][1]-_rgb[t0][1]))*_bright)>>8
        b = round((_rgb[t0][2] + (t-t0)*(_rgb[t0+1][2]-_rgb[t0][2]))*_bright)>>8
        _neopixel[(i + _offset) % _num] = (r, g, b)

def liushuideng():
    global m, time_on
    make_rainbow(my_rgb1, 23, 50, m)
    make_rainbow(my_rgb2, 23, 50, m)
    my_rgb1.write()
    my_rgb2.write()
    time.sleep(0.5)
    m = m + 1

time_on = None
while True:
    if time_on == None:
        time_on = time.time()
    oled.fill(0)
    oled.DispChar(str(time.time() - time_on), 1, 1)
    oled.show()
    if time.time() - time_on > 10 and time.time() - time_on <= 30:
        my_rgb1.fill( (255, 0, 0) )
        my_rgb2.fill( (255, 0, 0) )
        my_rgb1.write()
        my_rgb2.write()
        sleep_ms(50)
        my_rgb1.fill( (0, 0, 0) )
        my_rgb2.fill( (0, 0, 0) )
        my_rgb1.write()
        my_rgb2.write()
        sleep_ms(50)
        my_rgb1.fill( (255, 0, 0) )
        my_rgb2.fill( (255, 0, 0) )
        my_rgb1.write()
        my_rgb2.write()
        sleep_ms(50)
        my_rgb1.fill( (0, 0, 0) )
        my_rgb2.fill( (0, 0, 0) )
        my_rgb1.write()
        my_rgb2.write()
        sleep_ms(50)
        my_rgb1.fill( (0, 0, 255) )
        my_rgb2.fill( (0, 0, 255) )
        my_rgb1.write()
        my_rgb2.write()
        sleep_ms(50)
        my_rgb1.fill( (0, 0, 0) )
        my_rgb2.fill( (0, 0, 0) )
        my_rgb1.write()
        my_rgb2.write()
        sleep_ms(50)
        my_rgb1.fill( (0, 0, 255) )
        my_rgb2.fill( (0, 0, 255) )
        my_rgb1.write()
        my_rgb2.write()
        sleep_ms(50)
        my_rgb1.fill( (0, 0, 0) )
        my_rgb2.fill( (0, 0, 0) )
        my_rgb1.write()
        my_rgb2.write()
        sleep_ms(50)
        my_rgb1.fill( (255, 255, 255) )
        my_rgb2.fill( (255, 255, 255) )
        my_rgb1.write()
        my_rgb2.write()
        sleep_ms(50)
        my_rgb1.fill( (0, 0, 0) )
        my_rgb2.fill( (0, 0, 0) )
        my_rgb1.write()
        my_rgb2.write()
        sleep_ms(50)
        my_rgb1.fill( (255, 255, 255) )
        my_rgb2.fill( (255, 255, 255) )
        my_rgb1.write()
        my_rgb2.write()
        sleep_ms(50)
        my_rgb1.fill( (0, 0, 0) )
        my_rgb2.fill( (0, 0, 0) )
        my_rgb1.write()
        my_rgb2.write()
        sleep_ms(50)
        time.sleep(0.8)
    elif time.time() - time_on > 30:
        my_rgb1.fill((50,50,50))
        my_rgb2.fill((50,50,50))
        my_rgb2.write()
        my_rgb1.write()
        time.sleep(1)
    common()
