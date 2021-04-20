#mPythonType:0
# from machine import UART
from nplus.ai import *
from mpython import *

# p14 = MPythonPin(14, PinMode.IN)
uart1 = machine.UART(1, baudrate=9600, tx=Pin.P11, rx=Pin.P16)
ai = NPLUS_AI()
ai.mode_change(1)
import time
# i = 0
while True:
    if p14.read_digital() == 1:
        if uart1.any() and i == 0:
            time.sleep(0.5)
            my_list = uart1.readline()
            if 'GNGLL' in my_list:
                print(my_list)
                i = i + 1
    ai.picture_capture(0)
    time.sleep(1)
