from machine import UART
from mpython import *
import math
import network
import music
import neopixel
import time
import urequests
import audio


#引脚：
#p15tx&p16rx：串口uart2(SIM卡模块)
#p11tx&p14rx：串口uart1(北斗定位模块)——测试用的是北斗，北斗只输入14tx引脚不输出
#p0: "带我回家"按钮
#p1：照明灯开关
#p13：灯带1（灯数：63）
#p14：灯带2（灯数：63）


#摔倒判断：
# x轴加速度是否小于0.5（平行于屏幕方向向下为正方向）


#位置获取：
# 使用高德地图api 
# a: list
# b, c: float
# a1b1c1为纬度数据，a2b2c2为经度数据


# 实时定位位置：
# loc_get1, location1, a/b/c:1&2

p0 = MPythonPin(0, PinMode.IN)


#搭建WiFi，连接app用户手机数据
my_wifi = wifi()
my_wifi.connectWiFi("QFCS-MI", "999999999")


#路径规划初始化
NAV_URL = 'http://restapi.amap.com/v3/direction/walking?origin='
key_dy = '10d4ac81004a9581c1d9de89eac4035b'


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
lat_now = 0
lon_now = 0
loc_info = ''
loc_cycle = ''
location1 = []
a1 = []
a2 = []
b1 = 0
b2 = 0
c1 = 0
c2 = 0

stop = 0
st = 0

oled.fill(0)
oled.DispChar('初始化完毕', 0, 0)
oled.show()

# B键带我回家
def on_button_b_pressed(_):
    global backhome
    backhome += 1
    print(backhome)

button_b.event_pressed = on_button_b_pressed

#"带你回家"
def take_u_home():
    global stop, st, backhome, loc_cycle, method, _f, para_nav, nav, NAV_URL, lat_now, lon_now, ori_loc, data_audio, nav_file, r_audio 

    if backhome % 2 == 1:
        stop = 1
        
        # debug3
        print('开始导航')
        
        if st == 0:
            ori_loc = loc_cycle
            st = 1
        elif st == 1:
            ori_loc = '113.937507,22.570334'
            st = 0
            
        # oled.fill(0)
        # oled.DispChar('当前位置记录完毕', 0, 16)
        # oled.DispChar(ori_loc, 0, 32)
        # oled.show()
        # time.sleep(3)
        # oled.fill(0)
        # oled.show()
        print(ori_loc)
        
        para_nav = ori_loc+'&destination='+home_loc+'&key='+key_dy
        print(NAV_URL+str(para_nav))
        nav = urequests.get(url=NAV_URL+str(para_nav))
        print(nav)
        nav = nav.json()
        print(nav)
        if nav.get('status') == "1":
            # oled.fill(0)
            # oled.DispChar('守护者云拐杖', 24, 16)
            # oled.DispChar('正在带您回家', 24, 40)
            # oled.show()
            
            method = nav.get('route').get('paths')[0].get('steps')[0].get('instruction')
            
            # debug4
            # oled.fill(0)
            # oled.DispChar(method, 0, 0, 1, True)
            # oled.show()
            print(method)
            
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
            
            time.sleep(5)
            audio.stop()

            if nav.get('route').get('paths')[0].get('steps')[0].get('assistant_action') == "到达目的地":
                
                # TEST7
                # oled.fill(0)
                # oled.DispChar('守护者云拐杖', 24, 16)
                # oled.DispChar('导航结束', 40, 32)
                # oled.show()
                
                audio.play('nav_end.mp3')
                time.sleep(3)
                audio.stop()
                
                backhome = 0

    elif backhome % 2 == 0:
        print('停了')
        if stop == 1:
            rgb.fill((int(0), int(0), int(255)))
            rgb.write()
            time.sleep(2)
            rgb.fill( (0, 0, 0) )
            rgb.write()
            time.sleep_ms(1)
            stop = 0
        elif stop == 0:
            oled.fill(0)
            oled.DispChar('等待导航', 0, 0)
            oled.show()


audio.player_init(i2c)
audio.set_volume(100)
    
lon_now = 113.937507
lat_now = 22.570334
loc_cycle = str(lon_now) + ',' + str(lat_now)
home_loc = '113.931577,22.487280'
while True:
    take_u_home()
