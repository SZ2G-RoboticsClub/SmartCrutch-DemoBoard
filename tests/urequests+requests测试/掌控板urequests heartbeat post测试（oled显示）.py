from mpython import *
import urequests
import network
import time
# import ntptime

my_wifi = wifi()
my_wifi.connectWiFi('QFCS-MI', '999999999')
# ntptime.settime(8, "time.windows.com")
oled.fill(0)
oled.DispChar('初始化成功', 0, 0)
oled.show()


BASE_URL = 'http://192.168.31.132:8000/demoboard'
uuid = 'dytest'
status = 'ok'
# heartbeat_Loc = None
# heartbeat_time = None

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
        # heartbeat_time = None
        heartbeat_Loc = {"latitude": 22.576035, "longitude": 113.943418, "info": 'ahhhhhh'}
        # heartbeat_Loc = {"latitude": 22.576035, "longitude": 113.943418}
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
        # heartbeat_time = None
        
        print('没有问题3')
        
        if resp.get('code') == 0:                   #返回数据类型正常
            continue
        elif resp.get('code') == 1:
            print('拐杖未注册')
        else:
            oled.fill(0)
            oled.DispChar('心跳包错误', 0, 0, 1)
            # oled.DispChar(str(resp.get('msg')), 0, 16, 1, True) #查看是否正常回应
            oled.show()


