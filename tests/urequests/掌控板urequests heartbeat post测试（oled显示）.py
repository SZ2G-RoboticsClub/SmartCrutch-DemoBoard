from mpython import *
import urequests
import network
import time
import ntptime

my_wifi = wifi()
my_wifi.connectWiFi('QFCS-MI', '999999999')
ntptime.settime(8, "time.windows.com")
oled.fill(0)
oled.DispChar('初始化成功', 0, 0)
oled.show()


BASE_URL = 'http://39.103.138.199:5283/demoboard'
uuid = 'testuuid'
status = 'ok'
heartbeat_Loc = None
# heartbeat_time = None

time_set = None
lock = 0


def heartbeat():
    global uuid, status, heartbeat_Loc, heartbeat_time, data, resp
    data = {                #心跳包数据存储
    "uuid": uuid,
    "status": status,
    "loc": heartbeat_Loc,
    # "falltime": heartbeat_time
    }

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
    
    if button_b.is_pressed():
        rgb.fill( (int(255), int(255), int(255)) )
        rgb.write()
        status = 'emergency'
        heartbeat_Loc = {"latitude": 22.551343, "longitude": 114.063825}
        # if lock == 0:
        #     date_list = [time.localtime()[0], '年', time.localtime()[1], '月', time.localtime()[2], '日']
        #     time_list = [time.localtime()[3], '时', time.localtime()[4], '分', time.localtime()[5], '秒']
        #     f_date = ''.join(str(a) for a in date_list)
        #     f_time = ''.join(str(b) for b in time_list)

        #     lock = 1
        # print(f_date)
        # print(f_time)
        # heartbeat_time = {"date": f_date, "time": f_time}
        # oled.fill(0)
        # oled.DispChar((str(heartbeat_time), 0, 32, 1)
        # oled.show()
    else:
        rgb.fill( (0, 0, 0) )
        rgb.write()
        # heartbeat_time = None
        heartbeat_Loc = {"latitude": 22.576035, "longitude": 113.943418}
        status = 'ok'
    
    # print('没有问题2')
    # print(time.time() - time_set)
    
    if time.time() - time_set >= 5:
        heartbeat()

        oled.fill(0)
        oled.DispChar(str(data.get('status')), 0, 0)
        oled.DispChar(str(resp), 0, 16, 1, True)
        oled.show()

        time_set = None
        status = 'ok'
        heartbeat_Loc = None
        # heartbeat_time = None
        
        # print('没有问题3')
        
        if resp.get('code') == 0:                   #返回数据类型正常
            continue
        elif resp.get('code') == 1:
            print('拐杖未注册')
        else:
            oled.fill(0)
            oled.DispChar('心跳包错误', 0, 0, 1)
            oled.DispChar(str(resp.get('msg')), 0, 16, 1, True) #查看是否正常回应
            oled.show()


    
