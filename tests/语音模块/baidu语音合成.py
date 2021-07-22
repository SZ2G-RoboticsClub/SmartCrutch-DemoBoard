from mpython import *
import audio
import network
import urequests
import time
import gc

my_wifi = wifi()
my_wifi.connectWiFi('QFCS-MI', '999999999')

p2 = MPythonPin(2, PinMode.IN)

audio.player_init(i2c)
audio.set_volume(100)
file = 'nav_file.mp3'
baidu_params = {
    "API_Key": 'Lcr1un815AuFGa7DZDQv1sqx', 
    "Secret_Key": 'ujfZqO3mgcQZ52nXsfC9je02IiRDjaFb', 
    "text": '沿创科路向南步行174米右转', 
    "filename": file
}

_rsp = urequests.post("http://119.23.66.134:8085/baidu_tts", params=baidu_params)
with open(file, "w") as _f:
    while True:
        dat = _rsp.recv(1024)
        if not dat:
            break
        _f.write(dat)

print('ok')
while True:
    gc.collect()
    if p2.read_digital() == 1:
        print('现在开始')
        time.sleep(1)
        audio.play(file)
        time.sleep(1)

