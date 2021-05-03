from mpython import *
import network
import urequests
import time

uuid = '3141592653589793'
status = 'ok'
heartbeat_Loc = None

def heartbeat():
    global uuid, status, heartbeat_Loc
    data = {                #心跳包数据存储
    "uuid": uuid,
    "status":status,
    "loc": heartbeat_Loc
    }

    resp = urequests.post(url=BASE_URL+'/heartbeat', json=data)       #发送心跳包

    resp = resp.json()

while True:
    if time_set == None:
        time_set = time.time()

    if button_a.is_pressed():
        status = 'emergency'
        heartbeat_Loc = {
            "latitude": 22.5734267,
            "longitude": 114.1235464
        }

    if time.time() - time_set >= 5:
        heartbeat()
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