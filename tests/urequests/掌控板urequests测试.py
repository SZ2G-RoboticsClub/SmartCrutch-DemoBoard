from mpython import *
import urequests
import network
import time

my_wifi = wifi()
my_wifi.connectWiFi("QFCS-MI","999999999")

BASE_URL = 'http://192.168.31.125:8000/demoboard'
uuid = '3141592653589793'

s = urequests.get(url=BASE_URL+'/get_settings/'+uuid)
print(s)
time.sleep(1)
print(s.json())

oled.fill(0)
oled.DispChar(str(s.json()), 0, 0)
oled.show()