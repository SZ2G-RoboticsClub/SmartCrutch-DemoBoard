import urequests
from mpython import *
import time

my_wifi = wifi()
my_wifi.connectWiFi('啊哈','dy666821')

BASE_URL = 'http://192.168.43.199:8000/demoboard'
uuid = "3141592653589793"

data = {
        "uuid": uuid,
        "status": "emergency",
        "loc": {
            "latitude": -23.5,
            "longtitude": 2
            }
        }

s = urequests.post(url=BASE_URL+'/heartbeat', json=data)
# 响应的内容
print(s)
time.sleep(1)
print(s.json())


