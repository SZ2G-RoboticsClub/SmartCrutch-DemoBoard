#mPythonType:0
from mpython import *

import network

my_wifi = wifi()

my_wifi.connectWiFi('QFCS-MI', '999999999')

import audio

import urequests
oled.fill(0)
import gc;gc.collect()
audio.player_init(i2c)
audio.set_volume(100)
baidu_params = {"API_Key":'Lcr1un815AuFGa7DZDQv1sqx', "Secret_Key":'ujfZqO3mgcQZ52nXsfC9je02IiRDjaFb', "text":'开始导航。向东步行50米右转', "filename":'nav_file.mp3'}
_rsp = urequests.post("http://119.23.66.134:8085/baidu_tts", params=baidu_params)
with open('nav_file.mp3', "w") as _f:
    while True:
        dat = _rsp.recv(1024)
        if not dat:
            break
        _f.write(dat)
audio.play('nav_file.mp3')
time.sleep(5)
