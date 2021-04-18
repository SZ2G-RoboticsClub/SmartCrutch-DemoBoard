import urequests
from mpython import *

my_wifi = wifi()
my_wifi.connectWiFi('啊哈','dy666821')

# http get方法
r = urequests.get('http://micropython.org/ks/test.html')
# 响应的内容
r.content


# response：
# 刷入成功
# Connection WiFi.....
# WiFi(啊哈,-53dBm) Connection Successful, Config:('192.168.43.131', '255.255.255.0', '192.168.43.1', '192.168.43.1')
# MicroPython v2.1.2 on 2020-11-18; mpython with ESP32
