from mpython import *
from machine import UART
import time

uart1 = machine.UART(1, baudrate=9600, tx=Pin.P13, rx=Pin.P14)

while True:
    if uart1.any():
        print(uart1.readline())
