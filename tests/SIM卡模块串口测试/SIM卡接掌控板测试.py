#mPythonType:0
from machine import UART

from mpython import *

uart1 = machine.UART(1, baudrate=9600, tx=Pin.P16, rx=Pin.P15)

import time
print('开始')
time.sleep(2)
print('初始化成功')
i = 0
uart1.write('AT+SETVOLTE=1')
uart1.write('ATD18823340233')
# uart1.write('AT+CGMI')
while True:
    if uart1.any():
        m = uart1.readline()
        print(m)
        if 'OK' in m:
            print('ok!')
            time.sleep(1)
            break
    else:
        print('串口无数据，次数：' + str(i))
    i = i + 1
    time.sleep(0.1)
    if i >= 300:
        break

time.sleep(2)
print("\r\n" + '串口响应结束')
