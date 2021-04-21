from mpython import *
import urequests
import network
import time

my_wifi = wifi()
my_wifi.connectWiFi("QFCS-MI","999999999")

BASE_URL = 'http://192.168.31.125:8000/demoboard'
uuid = '3141592653589793'
status = 'ok'
heartbeat_Loc = None


while True:
    data = {                #心跳包数据存储
    "uuid": uuid,
    "status":status,
    "loc": heartbeat_Loc
    }
    
    r = urequests.post(url=BASE_URL+'/heartbeat', json=data) 

    # if resp.code != 200:                    #服务器读取数据错误或无法连接
    #     print('服务器数据传输发生错误')
    #     continue

    resp = resp.json()

    time.sleep(5)

    if resp['code'] == 0:                   #返回数据类型正常
        continue
    elif resp['code'] == 1:
        print('拐杖未注册')
        continue
    else:
        print(resp['msg'])          #查看是否正常回应