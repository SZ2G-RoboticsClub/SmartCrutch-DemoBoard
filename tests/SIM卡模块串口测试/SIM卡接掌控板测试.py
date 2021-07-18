#mPythonType:0
from machine import UART

from mpython import *

uart1 = machine.UART(1, baudrate=9600, tx=Pin.P16, rx=Pin.P9)

import time
print('开始')
time.sleep(2)
print('初始化成功')
i = 0

# uart1.write('AT+CGMI')
while True:
    uart1.write('AT+CPIN\n')
    if uart1.any():
        m = uart1.read()
        print(m)    
        break
    else:
        print('串口无数据，次数：' + str(i))
    i = i + 1
    time.sleep(0.1)
    if i >= 300:
        break

time.sleep(1)
print("\r\n" + '串口响应结束')
