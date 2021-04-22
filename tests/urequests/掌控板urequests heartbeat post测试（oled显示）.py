from mpython import *
import urequests
import network
import time

my_wifi = wifi()
my_wifi.connectWiFi("QFCS-MI","999999999")
oled.fill(0)
oled.DispChar('wifi连接成功', 0, 0)
oled.show()
time.sleep(2)
oled.fill(0)


BASE_URL = 'http://192.168.31.125:8000/demoboard'
uuid = '3141592653589793'


resp = 0
i = 0

while True:
    if button_b.is_pressed():
        i = i + 1
        
    if i % 2 == 1:
        rgb[1] = (255, 255, 255)
        rgb.write()
        status = 'emergency'
        heartbeat_Loc = {
            "latitude": 22.573933,
            "longitude": 113.933342
        }
    if i % 2 == 0:
        rgb[1] = (0, 0, 0)
        rgb.write()
        status = 'ok'
        heartbeat_Loc = None
    
    data = {                #心跳包数据存储
        "uuid": uuid,
        "status":status,
        "loc": heartbeat_Loc
    }
    
    r = urequests.post(url=BASE_URL+'/heartbeat', json=data) 
    
    resp = r.json()
    
    oled.fill(0)
    oled.DispChar('ok', 0, 1)
    oled.show()
    time.sleep(2)
    oled.fill(0)
    
    # if r.code != 200:           #服务器读取数据错误或无法连接
    #     print('服务器数据传输发生错误')
    #     continue

    oled.DispChar(str(resp), 0, 16, 1, True)
    oled.show()
    time.sleep(3)

    if resp['code'] == 0:                   #返回数据类型正常
        i = 0
        continue
    elif resp['code'] == 1:
        print('拐杖未注册')
        continue
    else:
        print(resp['msg'])          #查看是否正常回应
    
    
