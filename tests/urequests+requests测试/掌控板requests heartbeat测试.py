from mpython import *
import requests
import network
import time


my_wifi = wifi()
my_wifi.connectWiFi('Tenda_7C8540', '31832352')

#初始化服务器传输

# 本地
# BASE_URL = 'http://192.168.1.105:8000/demoboard'     #QFCS1
# BASE_URL = 'http://192.168.1.107:8000/demoboard'     #QFCS2
BASE_URL = 'http://192.168.31.131:8000/demoboard'    #QFCS-MI
# BASE_URL = 'http://192.168.43.199:8000/demoboard'    #idk
# BASE_URL = 'http://192.168.0.110:8000/demoboard'     #Tenda_7C8540

# 公网服务器
# BASE_URL = 'http://39.103.138.199:8000/demoboard'


oled.fill(0)
oled.DispChar('初始化成功', 0, 0)
oled.show()


uuid = 'dytest'
status = 'ok'
heartbeat_Loc = None


time_set = None
lock = 0


def heartbeat():
    global uuid, status, heartbeat_Loc, heartbeat_time, data, resp
    
    data = {                #心跳包数据存储
        "uuid": uuid,
        "status": status,
        "loc": heartbeat_Loc
    }
    
    print(data)
    resp = urequests.post(url=BASE_URL+'/heartbeat', json=data)       #发送心跳包
    resp = resp.json()


oled.fill(0)
oled.DispChar('开始循环', 0, 0)
oled.show()
time.sleep(2)
oled.fill(0)
oled.show()
while True:
    if time_set == None:
        time_set = time.time()
    
    # print('没有问题1')
    
    if button_a.is_pressed():
        rgb.fill( (int(255), int(255), int(255)) )
        rgb.write()
        status = 'emergency'
    else:
        rgb.fill( (0, 0, 0) )
        rgb.write()
        heartbeat_Loc = {"latitude": 22.576035, "longitude": 113.943418, "info": '深圳市第二高级中学'}
        status = 'ok'
    
    # print('没有问题2')
    # print(time.time() - time_set)
    
    if time.time() - time_set >= 5:
        heartbeat()

        oled.fill(0)
        oled.DispChar(str(data.get('status')), 0, 0)
        oled.DispChar(str(resp), 0, 16, 1, True)
        oled.show()
        
        print(resp)

        time_set = None
        status = 'ok'
        heartbeat_Loc = None
        
        print('没有问题3')
        
        if resp.get('code') == 0:                   #返回数据类型正常
            continue
        elif resp.get('code') == 1:
            print('拐杖未注册')
        else:
            oled.fill(0)
            oled.DispChar('心跳包错误', 0, 0, 1)
            oled.show()


