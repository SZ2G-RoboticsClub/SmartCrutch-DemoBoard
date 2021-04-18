#mPythonType:0
from machine import UART

from mpython import *

uart1 = machine.UART(1, baudrate=9600, tx=Pin.P16, rx=Pin.P15)

import time
i = 0
while True:
    if uart1.any() and i == 0:
        time.sleep(0.5)
        my_list = uart1.readline()
        if 'GNGLL' in my_list:
            print(my_list)
            i = i + 1
