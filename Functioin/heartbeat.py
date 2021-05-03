from mpython import *
import network
import urequests
import time

my_wifi = wifi()
my_wifi.connectWiFi('啊哈', 'dy666821')

oled.fill(0)
oled.DispChar('初始化成功', 0, 0)
oled.show()
time.sleep(2)
oled.fill(0)
oled.show()

BASE_URL = 'http://192.168.43.199:8000/demoboard'
uuid = '3141592653589793'
status = 'ok'
heartbeat_Loc = None
time_set = None

def heartbeat():
    global uuid, status, heartbeat_Loc, data, resp
    data = {                #心跳包数据存储
    "uuid": uuid,
    "status":status,
    "loc": heartbeat_Loc
    }

    resp = urequests.post(url=BASE_URL+'/heartbeat', json=data)       #发送心跳包

    resp = resp.json()


oled.fill(0)
oled.DispChar('开始循环', 0, 0, 1)
oled.show()
time.sleep(2)
oled.fill(0)
oled.show()
while True:
    if time_set == None:
        time_set = time.time()

    if button_a.is_pressed():
        rgb.fill((255, 255, 255))
        rgb.write()
        time.sleep_ms(1)
        status = 'emergency'
        heartbeat_Loc = {
            "latitude": 22.5734267,
            "longitude": 114.1235464
        }
    else:
        status = 'ok'
        heartbeat_Loc = None
        rgb.fill((0, 0, 0))
        rgb.write()

    if time.time() - time_set >= 5:
        heartbeat()
        oled.fill(0)
        oled.DispChar(str(data.get('status')), 0, 0, 1)
        oled.DispChar(str(resp), 0, 16, 1, True)
        oled.show()
        time_set = None
        if resp.get('code') == 0:                   #返回数据类型正常
            continue
        elif resp.get('code') == 1:
            print('拐杖未注册')
        else:
            oled.fill(0)
            oled.DispChar('心跳包错误', 0, 0, 1)
            oled.DispChar(str(resp.get('msg')), 0, 16, 1, True) #查看是否正常回应
            oled.show()