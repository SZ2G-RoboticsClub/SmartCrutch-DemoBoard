#mPythonType:0
from machine import UART
from mpython import *
from ai import *
import time



print('开始')
ai = NPLUS_AI()
print('初始化成功')
i = 0

uart2 = machine.UART(2, baudrate=115200, tx=Pin.P1, rx=Pin.P0)

# uart1.write('AT+CGMI')
# ai = NPLUS_AI()
while True:
    ai.AI_WaitForARP(0x34,[0])
    time.sleep(1)
    uart2.write('AT\n')
    time.sleep(1)
    # uart2.write('ATD13724285352;\n')
    if uart2.any():
        m = uart2.read()
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
