from mpython import *
import neopixel
import time

my_rgb = neopixel.NeoPixel(Pin(Pin.P13), n=24, bpp=3, timing=1)

def flashlight():                                                  
    for i in range(2):
        my_rgb.fill( (255, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (255, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 255) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 255) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (255, 255, 255) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)


while True:
    flashlight()
    time.sleep(2)