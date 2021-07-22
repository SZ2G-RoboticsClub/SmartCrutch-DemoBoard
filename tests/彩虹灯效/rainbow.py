#mPythonType:0
from mpython import *

import neopixel

p2 = MPythonPin(2, PinMode.IN)
p3 = MPythonPin(3, PinMode.ANALOG)

my_rgb1 = neopixel.NeoPixel(Pin(Pin.P7), n=63, bpp=3, timing=1)
my_rgb2 = neopixel.NeoPixel(Pin(Pin.P15), n=63, bpp=3, timing=1)

# my_rgb1 = neopixel.NeoPixel(Pin(Pin.P7), n=24, bpp=3, timing=1)
# my_rgb2 = neopixel.NeoPixel(Pin(Pin.P15), n=24, bpp=3, timing=1)


move = 0
switch = 0

def make_rainbow(_neopixel, _num, _bright, _offset):          
    _rgb = ((255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,255,255), (0,0,255), (136,0,255), (255,0,0))
    for i in range(_num):
        t = 7 * i / _num
        t0 = int(t)
        r = round((_rgb[t0][0] + (t-t0)*(_rgb[t0+1][0]-_rgb[t0][0]))*_bright)>>8
        g = round((_rgb[t0][1] + (t-t0)*(_rgb[t0+1][1]-_rgb[t0][1]))*_bright)>>8
        b = round((_rgb[t0][2] + (t-t0)*(_rgb[t0+1][2]-_rgb[t0][2]))*_bright)>>8
        _neopixel[(i + _offset) % _num] = (r, g, b)
    
        
def rainbow():
    global move
    make_rainbow(my_rgb1, 63, 80, move)
    make_rainbow(my_rgb2, 63, 80, move)
    
    # make_rainbow(my_rgb1, 24, 80, move)
    # make_rainbow(my_rgb2, 24, 80, move)
    
    my_rgb1.write()
    my_rgb2.write()
    # time.sleep(0.25)  
    move = move - 1
    
    
while True:
    # debug1
    print(p3.read_analog())
    
    if p2.read_digital() == 1:      # 开关灯
        switch += 1
        time.sleep_ms(350)
    #光感手电
    if switch % 3 == 0:
        my_rgb2.fill((0,0,0))
        my_rgb1.fill((0,0,0))
        my_rgb1.write()
        my_rgb2.write()
    elif switch % 3 == 1:
        if p3.read_analog() < 300:
            my_rgb1.fill( (255, 255, 255) )
            my_rgb2.fill( (255, 255, 255) )
            my_rgb1.write()
            my_rgb2.write()
            time.sleep_ms(500)
        elif p3.read_analog() >= 300:
            rainbow()    
    elif switch % 3 == 2:
        my_rgb1.fill( (255, 255, 255) )
        my_rgb2.fill( (255, 255, 255) )
        my_rgb1.write()
        my_rgb2.write()