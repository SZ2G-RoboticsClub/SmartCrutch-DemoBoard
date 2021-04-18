#mPythonType:0
from mpython import *
import time
import _thread
import neopixel
import sys

def torch_det():
    while True:
        oled.fill(0)
        oled.DispChar((str(light.read())), 0, 16, 1)
        oled.show()
        if light.read() < 60:
            rgb.fill((int(255), int(204), int(102)))
            rgb.write()
            time.sleep_ms(1)
        else:
            rgb.fill( (0, 0, 0) )
            rgb.write()
            time.sleep_ms(1)

my_rgb = neopixel.NeoPixel(Pin(Pin.P13), n=23, bpp=3, timing=1)

def light_on_off():
    while True:
        if button_a.is_pressed():
            my_rgb.fill( (0, 153, 0) )
            my_rgb.write()
        else:
            my_rgb.fill( (0, 0, 0) )
            my_rgb.write()


_thread.start_new_thread(torch_det,())
_thread.start_new_thread(light_on_off,())

    
