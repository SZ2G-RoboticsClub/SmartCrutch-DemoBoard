#mPythonType:0
from mpython import *

import time

import neopixel

my_rgb = neopixel.NeoPixel(Pin(Pin.P13), n=24, bpp=3, timing=1)

def thread1():
    thread1_count = 0
    while True:
        thread1_count = thread1_count + 1
        print('thread1:', thread1_count)
        oled.fill(0)
        oled.DispChar('Hello, world!', 0, 0, 1)
        oled.show()
        if button_b.was_pressed():
            oled.fill(0)
            oled.DispChar('Hello, world!', 0, 16, 1)
            oled.show()
        time.sleep(0.2)


def thread2():
    thread2_count = 0
    while True:
        thread2_count = thread2_count + 1
        print('thread2:', thread2_count)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        my_rgb.write()
        if button_a.was_pressed():
            my_rgb.fill( (255, 204, 0) )
            my_rgb.write()
        time.sleep(0.2)
        
        
_thread.start_new_thread(thread1, ())
_thread.start_new_thread(thread2, ())
