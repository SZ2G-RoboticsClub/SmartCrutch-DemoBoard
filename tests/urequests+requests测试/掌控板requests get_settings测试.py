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
# BASE_URL = 'http://192.168.31.131:8000/demoboard'    #QFCS-MI
# BASE_URL = 'http://192.168.43.199:8000/demoboard'    #idk
BASE_URL = 'http://192.168.0.110:8000/demoboard'     #Tenda_7C8540

# 公网服务器
# BASE_URL = 'http://39.103.138.199:8000/demoboard'


oled.fill(0)
oled.DispChar('初始化成功', 0, 0)
oled.show()


uuid = 'dytest'

s = urequests.get(url=BASE_URL+'/get_settings/'+uuid)
print(s)
time.sleep(1)
print(s.json())

oled.fill(0)
oled.DispChar(str(s.json()), 0, 0)
oled.show()