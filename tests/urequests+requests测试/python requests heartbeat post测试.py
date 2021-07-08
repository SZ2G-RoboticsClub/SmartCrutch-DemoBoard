import requests
import time
import keyboard
import math

# 本地
BASE_URL = 'http://0.0.0.0:8000/demoboard'


# 公网服务器
# BASE_URL = 'http://39.103.138.199:8000/demoboard'

uuid = 'fbb72bd8'
status = 'ok'
heartbeat_Loc = None


time_set = None
lock = 0


print('初始化成功')


def heartbeat():
    global uuid, status, heartbeat_Loc, data, resp
    data = {                #心跳包数据存储
    "uuid": uuid,
    "status": status,
    "loc": heartbeat_Loc
    }

    resp = requests.post(url=BASE_URL+'/heartbeat', json=data)       #发送心跳包

    resp = resp.json()



print('开始循环')


while True:
    if time_set == None:
        time_set = time.time()
        # print(time_set)
    
    print('没有问题1')

    m = '$GNGLL,2234.41586,N,11356.00044,E,051136.000,A,A*4E'
    location1 = m.split(',')
    
    if location1[2] == 'N':
        a1 = list(str(location1[1]))
        b1 = float(''.join(a1[2:]))
        c1 = ((100 - 0) / (60 - 0)) * (b1 - 0) + 0
        lat_now = math.floor(float(location1[1]) * 0.01) + c1 * 0.01
    elif location1[2] == 'S':
        a1 = list(str(location1[1]))
        b1 = float(''.join(a1[2:]))
        c1 = ((100 - 0) / (60 - 0)) * (b1 - 0) + 0
        lat_now = math.floor(float(location1[1]) * 0.01 * -1) + c1 * 0.01
    else:
        lat_now = 0


    if location1[4] == 'E':
        a2 = list(str(location1[3]))
        b2 = float(''.join(a2[3:]))
        c2 = ((100 - 0) / (60 - 0)) * (b2 - 0) + 0
        lon_now = math.floor(float(location1[3]) * 0.01) + c2 * 0.01
    elif location1[4] == 'W':
        a2 = list(str(location1[3]))
        b2 = float(''.join(a2[3:]))
        c2 = ((100 - 0) / (60 - 0)) * (b2 - 0) + 0
        lon_now = math.floor(float(location1[3]) * 0.01 * -1) + c2 * 0.01
    else:
        lon_now = 0


    if keyboard.is_pressed('space'):
        status = 'emergency'
        heartbeat_Loc = {
            "longitude": 114.063825, 
            "info": '不知道',
            "latitude": 22.551343
            }
    else:
        heartbeat_Loc = {
            "longitude": lon_now, 
            "info": '深圳市第二高级中学', 
            "latitude": lat_now
            }
        status = 'ok'

    
    # print('没有问题2')
    # print(time.time() - time_set)
    
    if time.time() - time_set >= 5:
        heartbeat()

        time_set = None

        print(status+'\n', heartbeat_Loc)
        print(data)
        print(resp)
        
        # print('没有问题3')
        
        if resp.get('code') == 0:                   #返回数据类型正常
            continue
        elif resp.get('code') == 1:
            print('拐杖未注册')
        else:
            print('心跳包错误')
            print(resp.get('msg')) #查看是否正常回应
