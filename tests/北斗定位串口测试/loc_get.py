#mPythonType:0
from mpython import *
from machine import UART
import time

uart1 = machine.UART(1, baudrate=9600, tx=Pin.P11, rx=Pin.P14)

# if button_a.was_pressed():
while True:
    loc_get4 = uart1.readline()
    print(loc_get4)
    location4 = (str(loc_get4).split(','))
    print(location4)
    if loc_get4 != None:
        #纬度存取，北正南负，赤道0°
        if location4[2] == 'N':
            a1 = list(str(location4[1]))
            b1 = float(''.join(a1[2:]))
            c1 = ((100 - 0) / (60 - 0)) * (b1 - 0) + 0
            lat_det = math.floor(float(location4[1]) * 0.01) + c1 * 0.01
        elif location4[2] == 'S':
            a1 = list(str(location4[1]))
            b1 = float(''.join(a1[2:]))
            c1 = ((100 - 0) / (60 - 0)) * (b1 - 0) + 0
            lat_det = math.floor(float(location4[1]) * 0.01 * -1) + c1 * 0.01
        else:
            lat_det = 0
        
        #经度存取，东正西负，否则0°
        if location4[4] == 'E':
            a2 = list(str(location4[3]))
            b2 = float(''.join(a2[3:]))
            c2 = ((100 - 0) / (60 - 0)) * (b2 - 0) + 0
            lon_det = math.floor(float(location4[3]) * 0.01) + c2 * 0.01
        elif location4[4] == 'W':
            a2 = list(str(location4[3]))
            b2 = float(''.join(a2[3:]))
            c2 = ((100 - 0) / (60 - 0)) * (b2 - 0) + 0
            lon_det = math.floor(float(location4[3]) * 0.01 * -1) + c2 * 0.01
        else:
            lon_det = 0
    
        det_loc = str(lat_det) + ',' + str(lon_det)
        print(det_loc)
        oled.fill(0)
        oled.DispChar(str(det_loc), 0, 0, 1, True)
        oled.show()
    else:
        oled.fill(0)
        oled.DispChar('无定位数据', 0, 0)
        oled.show()