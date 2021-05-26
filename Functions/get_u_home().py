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

# p1 = MPythonPin(1, PinMode.IN)
p0 = MPythonPin(0, PinMode.IN)
# my_rgb1 = neopixel.NeoPixel(Pin(Pin.P13), n=24, bpp=3, timing=1)
# my_rgb2 = neopixel.NeoPixel(Pin(Pin.P15), n=24, bpp=3, timing=1)


#心跳包数据初始化
# uuid = 'abfb6a0d'        #拐杖身份证
# status = 'ok'                      #拐杖状态（"ok"/"emergency"/"error"/"offline"）
# heartbeat_Loc = None             #location



#搭建WiFi，连接app用户手机数据
my_wifi = wifi()
my_wifi.connectWiFi("QFCS-MI","999999999")


#路径规划初始化
NAV_URL = 'https://restapi.amap.com/v3/direction/walking?'
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


#全局变量定义       
# switch = 0                                     
# move = 0        #彩虹灯变量
# down = 0        #0：拐杖没倒；    1：拐杖倒了
# fall = 0        #0：没摔倒；   1：摔倒了且已过了10s；    2：摔倒了30s
# time_on = None     #摔倒初始时间
# time_set = None    #心跳包发送初始时间
# dial = 0         #拨号：      1：已拨号一次         0：未拨过号



oled.fill(0)
oled.DispChar('初始化完毕', 0, 0)
oled.show()


#"带你回家"
def take_u_home():
    global backhome, loc_cycle, method, _f, para_nav, nav, NAV_URL, lat_now, lon_now, ori_loc, data_audio, nav_file, r_audio 
    
    if p0.read_digital() == 1:
        backhome = backhome + 1
    
    if backhome != 0:
        # fall_det()
        ori_loc = loc_cycle
        # oled.fill(0)
        # oled.DispChar('当前位置记录完毕', 0, 16)
        # oled.DispChar(ori_loc, 0, 32)
        # oled.show()
        # time.sleep(3)
        # oled.fill(0)
        # oled.show()
        print(ori_loc)
        print(home_loc)
        para_nav = 'origin='+ori_loc+'&destination='+home_loc+'&key='+key
        print(NAV_URL+para_nav)
        nav = urequests.get(url=NAV_URL+para_nav)
        # print(nav)
        nav = nav.json()
        print(nav)
        if nav.get('status') == "1":
            # oled.fill(0)
            # oled.DispChar(str(nav), 0, 0, 1, True)
            # oled.show()
            # time.sleep(5)
            # oled.fill(0)
            # oled.show()
            method = nav.get('route').get('paths')[0].get('steps')[0].get('instruction')
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
            # oled.fill(0)
            # oled.DispChar(method, 0, 0, 1, True)
            # oled.show()
            time.sleep(5)
        elif nav.get('status') != "1":
            # oled.fill(0)
            # oled.DispChar(str(nav), 0, 0, 1, True)
            # oled.show()
            # time.sleep(5)
            oled.fill(0)
            oled.DispChar('导航结束！', 0, 0)
            oled.show()
            time.sleep(2)
            oled.fill(0)
            oled.show()
            # audio.play('nav_end.mp3')
            # time.sleep(3)
            
            backhome = 0
                # break
            


# ============ Main ============

# ai = NPLUS_AI()
# ai.mode_change(1)
audio.player_init(i2c)
audio.set_volume(100)
# uart1 = machine.UART(1, baudrate=9600, tx=Pin.P11, rx=Pin.P14)
# uart2 = machine.UART(2, baudrate=9600, tx=Pin.P15, rx=Pin.P16)

#获得settingdata拐杖状态
# s = urequests.get(url=BASE_URL+'/get_settings/'+uuid)
# user_set = s.json()
# if user_set.get('code') == 0:
    # oled.DispChar('获取账户连接成功', 0, 0)
    # oled.show()
    # time.sleep(1)
    # oled.fill(0)
    # oled.show()
    
    #家庭住址经纬度获取
    # home = user_set.get('settings').get('home')
    # h = urequests.get(url=GEO_URL+home+'&output=json&key='+key)
    # h = h.json()

    # home_loc = h.get('geocodes')[0].get('location')
    # oled.DispChar('家庭位置记录完毕', 0, 16)
    # oled.DispChar(home_loc, 0, 32)
    # oled.show()
    # time.sleep(1)
    # oled.fill(0)
    # oled.show()
    
    
lon_now = 113.937507
lat_now = 22.570334
loc_cycle = str(lon_now) + ',' + str(lat_now)
home_loc = '113.931577,22.487280'
while True:
    take_u_home()
    
    
    
    # loc_get1 = uart1.readline()
    # location1 = (str(loc_get1).split(','))
    # if location1[2] == 'N':
    #     a1 = list(str(location1[1]))
    #     b1 = float(''.join(a1[2:]))
    #     c1 = ((100 - 0) / (60 - 0)) * (b1 - 0) + 0
    #     lat_now = math.floor(float(location1[1]) * 0.01) + c1 * 0.01
    # elif location1[2] == 'S':
    #     a1 = list(str(location1[1]))
    #     b1 = float(''.join(a1[2:]))
    #     c1 = ((100 - 0) / (60 - 0)) * (b1 - 0) + 0
    #     lat_now = math.floor(float(location1[1]) * 0.01 * -1) + c1 * 0.01
    # else:
    #     lat_now = 0


    # if location1[4] == 'E':
    #     a2 = list(str(location1[3]))
    #     b2 = float(''.join(a2[3:]))
    #     c2 = ((100 - 0) / (60 - 0)) * (b2 - 0) + 0
    #     lon_now = math.floor(float(location1[3]) * 0.01) + c2 * 0.01
    # elif location1[4] == 'W':
    #     a2 = list(str(location1[3]))
    #     b2 = float(''.join(a2[3:]))
    #     c2 = ((100 - 0) / (60 - 0)) * (b2 - 0) + 0
    #     lon_now = math.floor(float(location1[3]) * 0.01 * -1) + c2 * 0.01
    # else:
    #     lon_now = 0

    # TEST2
