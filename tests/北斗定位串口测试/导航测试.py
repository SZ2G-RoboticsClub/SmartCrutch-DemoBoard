#mPythonType:0
from mpython import *
from machine import UART
import time
import urequests
import json
import neopixel

my_rgb = neopixel.NeoPixel(Pin(Pin.P13), n=24, bpp=3, timing=1)

MAP_URL = 'http://api.map.baidu.com/directionlite/v1/walking?'
D_URL = 'https://api.map.baidu.com/routematrix/v2/walking?'
ak = 'CZHBGZ6TXADxI2UecA1xfpq2GtKLMYam'

my_wifi = wifi()
my_wifi.connectWiFi("QFCS-MI","999999999")
uart1 = machine.UART(1, baudrate=9600, tx=Pin.P11, rx=Pin.P14)

oled.fill(0)
oled.DispChar('初始化完毕', 0, 0)
oled.show()
time.sleep(2)
oled.fill(0)
oled.show()

backhome = 0
move = 0
distance = 0
des_loc = ''
ori_loc = ''
para1 = ''
para2 = ''
lat_first = 0
lon_first = 0
lat_now = 0
lon_now = 0
lat_det = 0
lon_det = 0
end_loc = ''
way = ''
l_way = []
location1 = []
location3 = []
location4 = []
p = 0
c = 0

while True:
    if touchPad_H.was_pressed():
        p = p + 1


    if p % 2 == 1:
        my_rgb.fill( (255, 255, 255) )
        my_rgb.write()
    elif p % 2 == 0:
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
    
    
    if button_b.was_pressed() and c == 0:
        while True:
            location1 = (str(uart1.readline()).split(','))
            if location1[2] == 'N':
                a7 = list(str(location1[1]))
                b7 = float(''.join(a7[2:]))
                c7 = ((100 - 0) / (60 - 0)) * (b7 - 0) + 0
                lat_first = math.floor(float(location1[1]) * 0.01) + c7 * 0.01
            elif location1[2] == 'S':
                a7 = list(str(location1[1]))
                b7 = float(''.join(a7[2:]))
                c7 = ((100 - 0) / (60 - 0)) * (b7 - 0) + 0
                lat_first = math.floor(float(location1[1]) * 0.01 * -1) + c7 * 0.01
            else:
                lat_first = 0

            if location1[4] == 'E':
                a8 = list(str(location1[3]))
                b8 = float(''.join(a8[3:]))
                c8 = ((100 - 0) / (60 - 0)) * (b8 - 0) + 0
                lon_first = math.floor(float(location1[3]) * 0.01) + c8 * 0.01
            elif location1[4] == 'W':
                a8 = list(str(location1[3]))
                b8 = float(''.join(a8[3:]))
                c8 = ((100 - 0) / (60 - 0)) * (b8 - 0) + 0
                lon_first = math.floor(float(location1[3]) * 0.01 * -1) + c8 * 0.01
            else:
                lon_first = 0

            des_loc = str(lat_first) + ',' + str(lon_first)
            print(des_loc)
            break
        backhome = 1
        c == 1
        oled.fill(0)
        oled.DispChar('初始位置记录完毕', 0, 16)
        oled.DispChar(des_loc, 0, 32)
        oled.show()
        time.sleep(1)
        oled.fill(0)
        oled.show()
                
    if button_a.was_pressed() and c == 1:
        while True:
            location3 = (str(uart1.readline()).split(','))
            if location3[2] == 'N':
                a5 = list(str(location3[1]))
                b5 = float(''.join(a5[2:]))
                c5 = ((100 - 0) / (60 - 0)) * (b5 - 0) + 0
                lat_now = math.floor(float(location3[1]) * 0.01) + c5 * 0.01
            elif location3[2] == 'S':
                a5 = list(str(location3[1]))
                b5 = float(''.join(a5[2:]))
                c5 = ((100 - 0) / (60 - 0)) * (b5 - 0) + 0
                lat_now = math.floor(float(location3[1]) * 0.01 * -1) + c5 * 0.01
            else:
                lat_now = 0
            
            #经度存取，东正西负，否则0°
            if location3[4] == 'E':
                a6 = list(str(location3[3]))
                b6 = float(''.join(a6[3:]))
                c6 = ((100 - 0) / (60 - 0)) * (b6 - 0) + 0
                lon_now = math.floor(float(location3[3]) * 0.01) + c6 * 0.01
            elif location3[4] == 'W':
                a6 = list(str(location3[3]))
                b6 = float(''.join(a6[3:]))
                c6 = ((100 - 0) / (60 - 0)) * (b6 - 0) + 0
                lon_now = math.floor(float(location3[3]) * 0.01 * -1) + c6 * 0.01
            else:
                lon_now = 0
            ori_loc = str(lat_now) + ',' + str(lon_now)
            print(ori_loc)
            break
        backhome = 1
        oled.fill(0)
        oled.DispChar('当前位置记录完毕', 0, 16)
        oled.DispChar(ori_loc, 0, 32)
        oled.show()
        time.sleep(1)
        backhome = 1
        oled.fill(0)
        oled.show()
        
    if backhome == 1:
        para1 = 'origin='+ori_loc+'&destination='+des_loc+'&ak='+ak
        nav = urequests.get(url=MAP_URL+str(para1))
        route = nav.json()
        method = route.get('result').get('routes')[0].get('steps')
        # print(method)
        for i in method:
            way = i.get('instruction').replace('<b>', '').replace('</b>', '')
            oled.fill(0)
            oled.DispChar(way, 0, 0, 1, True)
            oled.show()
            end_loc = i.get('end_location').get('lat') + ',' + i.get('end_location').get('lng')
            # time.sleep(5)
            while True:
                location4 = (str(uart1.readline()).split(','))
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
                para2 = 'output=json&origins='+det_loc+'&destinations='+end_loc+'&ak='+ak
                d = urequests.get(url=D_URL+para2)
                d = d.json()
                distance = d.get('result')[0].get('distance').get('value')
            
                if distance <= 10:
                    l_way = way.split(',')[-1]
                    oled.fill(0)
                    oled.DispChar(l_way, 0, 0, 1, True)
                    oled.show()
                    break