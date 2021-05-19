from machine import UART
from mpython import *
import math
import network
import music
import neopixel
import time
import urequests
import audio

my_wifi = wifi()
my_wifi.connectWiFi("QFCS-MI","999999999")

#路径规划初始化
GEO_URL = 'https://restapi.amap.com/v3/geocode/geo?address='
R_GEO_URL= 'https://restapi.amap.com/v3/geocode/regeo?output='
NAV_URL = 'https://restapi.amap.com/v3/direction/walking?origin='
key = '10d4ac81004a9581c1d9de89eac4035b'


api_key = 'Lcr1un815AuFGa7DZDQv1sqx'        #百度语音导航初始化
secret_key = 'ujfZqO3mgcQZ52nXsfC9je02IiRDjaFb'
method = ''
nav_file = 'nav_file.mp3'


lat_home = 0     #家庭住址经纬信息
lon_home = 0
home_loc = ''

backhome = 0
ori_loc = ''
para_nav = ''


#实时获取老人定位
lat_now = 22.568319
lon_now = 113.939018
loc_info = ''
loc_cycle = ''
location1 = []
a1 = []
a2 = []
b1 = 0
b2 = 0
c1 = 0
c2 = 0


#全局变量定义       
i = 0                                     
move = 0        #彩虹灯变量
down = 0        #0：拐杖没倒；    1：拐杖倒了
fall = 0        #0：没摔倒；   1：摔倒了且已过了10s；    2：摔倒了30s
time_on = None     #摔倒初始时间
time_set = None    #心跳包发送初始时间
dial = 0         #拨号：      1：已拨号一次         0：未拨过号


oled.fill(0)
oled.DispChar('初始化完毕', 0, 0)
oled.show()


home = "广东省深圳市南山区茶光1(公交站)"
h = urequests.get(url=GEO_URL+home+'&output=json&key='+key)
h = h.json()
home_loc = h.get('geocodes')[0].get('location')



def take_u_home():
    global loc_cycle, method, _dat, _f, para_nav, nav, route, ak, NAV_URL, lat_now, lon_now, ori_loc, data_audio, nav_file, r_audio 
    
    if p0.read_digital() == 1:
        backhome = backhome + 1
    
    if backhome != 0:
        ori_loc = str(lon_now) + ',' + str(lat_now)
        # oled.fill(0)
        # oled.DispChar('当前位置记录完毕', 0, 16)
        # oled.DispChar(ori_loc, 0, 32)
        # oled.show()
        # time.sleep(3)
        # oled.fill(0)
        # oled.show()
        # print(ori_loc)
        para_nav = 'origin='+ori_loc+'&destination='+home_loc+'&key='+key
        # print(para_nav)
        nav = urequests.get(url=NAV_URL+str(para_nav))
        # print(nav)
        nav = nav.json()
        # print(nav)
        if nav.get('status') == "1":
            # oled.fill(0)
            # oled.DispChar(str(nav), 0, 0, 1, True)
            # oled.show()
            # time.sleep(5)
            # oled.fill(0)
            # oled.show()
            method = nav.get('route').get('paths')[0].get('steps')[0].get('instruction')
            data_audio = {
                "API_Key": api_key,
                "Secret_Key": secret_key,
                "text": method,
                "filename": nav_file
            }
            r_audio = urequests.post("http://119.23.66.134:8085/baidu_tts", params=data_audio)
            with open(nav_file, "w") as _f:
                while True:
                    dat = r_audio.recv(1024)
                    if not dat:
                        break
                    _f.write(dat)
            audio.play(nav_file)
            # oled.fill(0)
            # oled.DispChar(method, 0, 0, 1, True)
            # oled.show()
            time.sleep(5)
        elif nav.get('status') != "1":
            # oled.fill(0)
            # oled.DispChar(str(nav), 0, 0, 1, True)
            # oled.show()
            # time.sleep(5)
            # oled.fill(0)
            oled.DispChar('导航结束！', 0, 0)
            oled.show()
            time.sleep(2)
            oled.fill(0)
            oled.show()
            # audio.play('nav_end.mp3')
            time.sleep(3)
            
            backhome = 0
                # break