from mpython import *
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
method = []
c = 0

#平常状态之彩虹灯效设定(ok)
def make_rainbow(_neopixel, _num, _bright, _offset):          
    _rgb = ((255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,255,255), (0,0,255), (136,0,255), (255,0,0))
    for i in range(_num):
        t = 7 * i / _num
        t0 = int(t)
        r = round((_rgb[t0][0] + (t-t0)*(_rgb[t0+1][0]-_rgb[t0][0]))*_bright)>>8
        g = round((_rgb[t0][1] + (t-t0)*(_rgb[t0+1][1]-_rgb[t0][1]))*_bright)>>8
        b = round((_rgb[t0][2] + (t-t0)*(_rgb[t0+1][2]-_rgb[t0][2]))*_bright)>>8
        _neopixel[(i + _offset) % _num] = (r, g, b)


#平常状态之流水彩虹灯(ok)
def rainbow():
    global move
    make_rainbow(my_rgb, 23, 80, move)
    my_rgb.write()
    time.sleep(0.25)
    move = move + 1
    

def common():
    oled.fill(0)
    oled.DispChar('守护者云拐杖', 24, 16)
    oled.DispChar('开', 56, 32)
    oled.show()
    #光感手电
    if light.read() < 20:
        my_rgb.fill( (255, 255, 255) )
        my_rgb.write()
    else:
        rainbow()
        
        
while True:
    common()
    if button_b.was_pressed() and c == 0:
        print('记录初始位置')
        while True:
            time.sleep(0.1)
            loc_get1 = uart1.readline()
            if 'GNGLL' in loc_get1:
                print(loc_get1)
                location1 = (str(loc_get1).split(','))
                if location1[2] == 'N':
                    lat_first = float(location1[1]) * 0.01
                elif location1[2] == 'S':
                    lat_first = float(location1[1]) * 0.01 * -1
                else:
                    lat_first = 0

                if location1[4] == 'E':
                    lon_first = float(location1[3]) * 0.01
                elif location1[4] == 'W':
                    lon_first = float(location1[3]) * 0.01 * -1
                else:
                    lon_first = 0
                des_loc = str(lat_first) + ',' + str(lon_first)
                c = 1
                print(loc_get1)
                print(des_loc)
                break
                
    if button_a.was_pressed() and c == 1:
        print('终止位置')
        while True:
            time.sleep(0.1)
            loc_get3 = uart1.readline()        #串口读取坐标
            if 'GNGLL' in loc_get3:            #过滤，只留GLL的格式
                print(loc_get3)
                location3 = (str(loc_get3).split(','))     #存取到列表
                #纬度存取，北正南负，赤道0°
                if location3[2] == 'N':
                    lat_now = float(location3[1]) * 0.01
                elif location3[2] == 'S':
                    lat_now = float(location3[1]) * 0.01 * -1
                else:
                    lat_now = 0
                
                #经度存取，东正西负，否则0°
                if location3[4] == 'E':
                    lon_now = float(location3[3]) * 0.01
                elif location3[4] == 'W':
                    lon_now = float(location3[3]) * 0.01 * -1
                else:
                    lon_now = 0
                ori_loc = str(lat_now) + ',' + str(lon_now)
                print(loc_get3)
                print(ori_loc)
                backhome = 1
                c = 0
                break
    
    if backhome == 1:
        para1 = 'origin='+ori_loc+'&destination='+des_loc+'&ak='+ak
        nav = urequests.get(url=MAP_URL+str(para1))
        route = nav.json()
        method = route.get('result').get('routes')[0].get('steps')
        print(method)
        for i in method:
            way = i.get('instruction').replace('<b>', '').replace('</b>', '')
            oled.fill(0)
            oled.DispChar(way, 0, 0, 1, True)
            oled.show()
            end_loc = i.get('end_location').get('lat') + ',' + i.get('end_location').get('lng')
            time.sleep(5)
            while True:
                time.sleep(0.1)
                loc_get4 = uart1.readline()       #串口读取坐标
                if 'GNGLL' in loc_get3:            #过滤，只留GLL的格式
                    location4 = (str(loc_get4).split(','))     #存取到列表
                    #纬度存取，北正南负，赤道0°
                    if location4[2] == 'N':
                        lat_det = float(location4[1]) * 0.01
                    elif location4[2] == 'S':
                        lat_det = float(location4[1]) * 0.01 * -1
                    else:
                        lat_det = 0
                    
                    #经度存取，东正西负，否则0°
                    if location4[4] == 'E':
                        lon_det = float(location4[3]) * 0.01
                    elif location4[4] == 'W':
                        lon_det = float(location4[3]) * 0.01 * -1
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

