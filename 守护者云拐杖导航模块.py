from mpython import *
import time
import urequests


MAP_URL = 'http://api.map.baidu.com/directionlite/v1/walking?'
D_URL = 'https://api.map.baidu.com/routematrix/v2/walking?'
ak = 'CZHBGZ6TXADxI2UecA1xfpq2GtKLMYam'

my_wifi = wifi()
my_wifi.connectWiFi("QFCS-MI","999999999")

backhome = 0
distance = 0
des_loc = ''
ori_loc = ''
para1 = ''
para2 = ''
lat_first = 0
lon_first = 0
lat_now = 0
lon_now = 0
loc_get1 = []
loc_get3 = []
loc_get4 = []
lat_det = 0
lon_det = 0
end_loc = ''
way = ''
l_way = []
location1 = []
location3 = []
location4 = []
method = []
while True:
    if button_b.was_pressed():
        if uart1.any():
            time.sleep(0.1)
            loc_get1 = uart1.readline()
            if 'GNGLL' in loc_get1:
                location1 = (str(loc_get1).split(','))
                if location1[2] == 'N':
                    lat_first = float(location1[1])
                elif location1[2] == 'S':
                    lat_first = float(location1[1]) * -1
                else:
                    lat_first = 0

                if location1[4] == 'E':
                    lon_first = float(location1[3])
                elif location1[4] == 'W':
                    lon_first = float(location1[3]) * -1
                else:
                    lon_first = 0
                des_loc = str(lat_first) + ',' + str(lon_first)
    elif button_a.was_pressed():
        if uart1.any():
            time.sleep(0.1)
            loc_get3 = uart1.readline()        #串口读取坐标
            if 'GNGLL' in loc_get3:            #过滤，只留GLL的格式
                location3 = (str(loc_get3).split(','))     #存取到列表
                #纬度存取，北正南负，赤道0°
                if location3[2] == 'N':
                    lat_now = float(location3[1])
                elif location3[2] == 'S':
                    lat_now = float(location3[1]) * -1
                else:
                    lat_now = 0
                
                #经度存取，东正西负，否则0°
                if location3[4] == 'E':
                    lon_now = float(location3[3])
                elif location3[4] == 'W':
                    lon_now = float(location3[3]) * -1
                else:
                    lon_now = 0
                ori_loc = str(lat_now) + ',' + str(lon_now)
            backhome = 1
    
    if backhome == 1:
        para1 = 'origin='+ori_loc+'&destination='+des_loc+'&ak='+ak
        route = requests.get(url=MAP_URL+str(para1))
        route = route.json()
        method = route.get('result').get('routes')[0].get('steps')
        for i in method:
            way = i.get('instruction').replace('<b>', '').replace('</b>', '')
            oled.fill(0)
            oled.DispChar(way, 0, 0, 1, True)
            oled.show()
            end_loc = i.get('end_location').get('lat') + ',' + i.get('end_location').get('lng')
            while True:
                if uart1.any():
                    time.sleep(0.1)
                    loc_get4 = uart1.readline()        #串口读取坐标
                    if 'GNGLL' in loc_get3:            #过滤，只留GLL的格式
                        location4 = (str(loc_get4).split(','))     #存取到列表
                        #纬度存取，北正南负，赤道0°
                        if location4[2] == 'N':
                            lat_det = float(location4[1])
                        elif location4[2] == 'S':
                            lat_det = float(location4[1]) * -1
                        else:
                            lat_det = 0
                        
                        #经度存取，东正西负，否则0°
                        if location4[4] == 'E':
                            lon_det = float(location4[3])
                        elif location4[4] == 'W':
                            lon_det = float(location4[3]) * -1
                        else:
                            lon_det = 0
                        det_loc = str(lat_det) + ',' + str(lon_det)
                para2 = 'output=json&origins='+det_loc+'&destinations='+end_loc+'&ak='+ak
                d = requests.get(url=D_URL+para2)
                d = d.json()
                distance = d.get('result')[0].get('distance').get('value')
                if distance <= 10:
                    l_way = way.split(',')[-1]
                    oled.fill(0)
                    oled.DispChar(l_way, 0, 0, 1, True)
                    oled.show()
                    break

