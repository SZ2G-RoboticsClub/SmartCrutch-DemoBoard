from mpython import *
import network
import audio
import time
import urequests
import neopixel
import gc;gc.collect()

# p0 = MPythonPin(0, PinMode.ANALOG)
my_rgb1 = neopixel.NeoPixel(Pin(Pin.P13), n=70, bpp=3, timing=1)
my_rgb2 = neopixel.NeoPixel(Pin(Pin.P15), n=70, bpp=3, timing=1)

my_wifi = wifi()
my_wifi.connectWiFi('idk', '12345678')

oled.fill(0)
oled.DispChar('初始化成功', 0, 0)
oled.show()
time.sleep(2)

def on_button_a_pressed(_):
    global mode
    mode = 1

def on_button_b_pressed(_):
    global mode
    mode = 2

button_a.event_pressed = on_button_a_pressed
button_b.event_pressed = on_button_b_pressed

audio.player_init(i2c)
audio.set_volume(100)
mode = 0

# my_rgb1.fill( (0,0,0) )
# my_rgb2.fill( (0,0,0) )

my_rgb1.fill( (255, 255, 255) )
my_rgb2.fill( (255, 255, 255) )
my_rgb1.write()
my_rgb2.write()

while True:
    if mode == 0:
        audio.stop()
        oled.fill(0)
        oled.DispChar('守护者云拐杖', 24, 16)
        oled.DispChar('开', 56, 32)
        oled.show()
        time.sleep(1)
        
    if mode == 1:
        oled.fill(0)
        oled.DispChar('守护者云拐杖', 24, 16)
        oled.DispChar('开始导航', 40, 32)
        oled.show()
        baidu_params = {"API_Key":'Lcr1un815AuFGa7DZDQv1sqx', "Secret_Key":'ujfZqO3mgcQZ52nXsfC9je02IiRDjaFb', "text":'开始导航。向南步行78米，左转', "filename":'nav_file.mp3'}
        _rsp = urequests.post("http://119.23.66.134:8085/baidu_tts", params=baidu_params)
        print(_rsp.json)
        with open('nav_file.mp3', "w") as _f:
            while True:
                dat = _rsp.recv(1024)
                if not dat:
                    break
                _f.write(dat)
        audio.play('nav_file.mp3')
        time.sleep(3)
        audio.stop()
        oled.fill(0)
        oled.DispChar('守护者云拐杖', 24, 16)
        oled.DispChar('正在带您回家', 24, 40)
        oled.show()
        time.sleep(5)
        mode = 0
        
        
    if mode == 2:   
        oled.fill(0)
        oled.show()
        time.sleep(5)
        oled.fill(0)
        oled.DispChar('守护者云拐杖', 24, 16)
        oled.DispChar('正在带您回家', 24, 40)
        oled.show()
        baidu_params = {"API_Key":'Lcr1un815AuFGa7DZDQv1sqx', "Secret_Key":'ujfZqO3mgcQZ52nXsfC9je02IiRDjaFb', "text":'向西步行55米', "filename":'nav_file.mp3'}
        _rsp2 = urequests.post("http://119.23.66.134:8085/baidu_tts", params=baidu_params)
        with open('nav_file.mp3', "w") as _f2:
            while True:
                dat2 = _rsp2.recv(1024)
                if not dat2:
                    break
                _f2.write(dat2)
        audio.play('nav_file.mp3')
        time.sleep(5)
        audio.stop()
        

        time.sleep(20)
        oled.fill(0)
        oled.DispChar('守护者云拐杖', 24, 16)
        oled.DispChar('导航结束', 40, 32)
        oled.show()
        # baidu_params = {"API_Key":'Lcr1un815AuFGa7DZDQv1sqx', "Secret_Key":'ujfZqO3mgcQZ52nXsfC9je02IiRDjaFb', "text":'导航结束', "filename":'nav_file.mp3'}
        # _rsp3 = urequests.post("http://119.23.66.134:8085/baidu_tts", params=baidu_params)
        # with open('nav_file.mp3', "w") as _f3:
        #     while True:
        #         dat3 = _rsp3.recv(1024)
        #         if not dat3:
        #             break
        #         _f3.write(dat3)
        audio.play('nav_end.mp3')
        time.sleep(2)
        audio.stop()
        mode = 0
