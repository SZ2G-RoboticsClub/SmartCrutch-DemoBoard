from mpython import *
import network
import urequests
import ubinascii
import time

my_wifi = wifi()
# my_wifi.connectWiFi('啊哈', 'dy666821')
my_wifi.connectWiFi('QFCS-MI', '999999999')

oled.fill(0)
oled.DispChar('初始化成功', 0, 0)
oled.show()
time.sleep(2)
oled.fill(0)
oled.show()



#初始化服务器传输

# 本地
# BASE_URL = 'http://192.168.1.104:8000/demoboard'     #QFCS1
# BASE_URL = 'http://192.168.1.107:8000/demoboard'     #QFCS2
BASE_URL = 'http://192.168.31.132:8000/demoboard'    #QFCS-MI
# BASE_URL = 'http://192.168.43.199:8000/demoboard'    #idk
# BASE_URL = 'http://192.168.0.110:8000/demoboard'     #Tenda_7C8540
# BASE_URL = 'http://192.168.103.87:8000/demoboard'    #啊哈

# 公网服务器
# BASE_URL = 'http://39.103.138.199:8000/demoboard'



uuid = 'fbb72bd8'
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
    
    loc_info = '深圳市第二高级中学'
        
    tran = ubinascii.hexlify(loc_info.encode('utf-8'))
    tran = tran.decode()

    if button_b.is_pressed():
        rgb.fill((255, 255, 255))
        rgb.write()
        time.sleep_ms(1)
        status = 'emergency'
        heartbeat_Loc = {
            "latitude": 22.570334,
            "longitude": 113.937507,
            "info": tran
        }
    else:
        status = 'ok'
        heartbeat_Loc = {
            "latitude": 22.570334,
            "longitude": 113.937507,
            "info": tran
        }
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