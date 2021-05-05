from mpython import *

import audio

import network

my_wifi = wifi()

my_wifi.connectWiFi('Tenda_7C8540', '31832352')

import urequests

import time

audio.player_init(i2c)
audio.set_volume(100)
file = 'nav_file.mp3'
baidu_params = {"API_Key":'Lcr1un815AuFGa7DZDQv1sqx', "Secret_Key":'ujfZqO3mgcQZ52nXsfC9je02IiRDjaFb', "text":'向前行驶8公里，然后左转，进入创科路，马上本次导航将要结束！', "filename":file}
_rsp = urequests.post("http://119.23.66.134:8085/baidu_tts", params=baidu_params)
with open(file, "w") as _f:
    while True:
        dat = _rsp.recv(1024)
        if not dat:
            break
        _f.write(dat)
audio.play(file)
print('现在开始')
time.sleep(1)
print('1s过了')
time.sleep(5)
print('5s过了')
