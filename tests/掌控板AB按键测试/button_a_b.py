#mPythonType:0
from mpython import *

import time

def on_button_a_pressed(_):
    global mode, switch, backhome
    rgb.fill( (0, 0, 0) )
    rgb.write()
    time.sleep_ms(1)
    rgb.fill((int(255), int(0), int(0)))
    rgb.write()
    time.sleep_ms(1)

button_a.event_pressed = on_button_a_pressed

def on_button_b_pressed(_):
    global mode, switch, backhome
    rgb.fill( (0, 0, 0) )
    rgb.write()
    time.sleep_ms(1)
    rgb.fill((int(51), int(255), int(51)))
    rgb.write()
    time.sleep_ms(1)

button_b.event_pressed = on_button_b_pressed
