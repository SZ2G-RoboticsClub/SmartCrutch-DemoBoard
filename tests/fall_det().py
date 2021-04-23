from machine import UART
from mpython import *
from bluebit import *
from nplus.ai import *
import math
import network
import music
import neopixel
import time
import urequests
import json

my_rgb = neopixel.NeoPixel(Pin(Pin.P13), n=24, bpp=3, timing=1)


#心跳包数据初始化
uuid = '3141592653589793'        #拐杖身份证
status = ""                      #拐杖状态（"ok"/"emergency"/"error"/"offline"）
heartbeat_Loc = None             #location


#初始化服务器传输
BASE_URL = 'http://192.168.43.199:8000/demoboard'
my_wifi = wifi()         #搭建WiFi，连接app用户手机数据
my_wifi.connectWiFi("idk","12345678")

oled.fill(0)
oled.DispChar('初始化完毕', 0, 0)
oled.show()
time.sleep(2)
oled.fill(0)
oled.show()

# #路径规划初始化
# MAP_URL = 'http://api.map.baidu.com/directionlite/v1/walking?'
# ak = 'CZHBGZ6TXADxI2UecA1xfpq2GtKLMYam'
# lat_first = 0     #出门获取的经纬信息
# lon_first = 0
# location1 = []
# loc_get1 = []
# des_loc = ''
# lat_now = 0       #按下带我回家按钮记录的经纬信息
# lon_now = 0
# location3 = []
# log_get3 = []
# ori_loc = ''
# para1 = ''



#全局变量定义                                            
backhome = 0    #1：按下带我回家按钮；   0：导航到家或空状态
move = 0        #彩虹灯变量
down = 0        #0：拐杖没倒；    1：拐杖倒了
fall = 0        #0：没摔倒；   1：摔倒了且已过了10s；    2：摔倒了30s
time_on = None     #摔倒初始时间
switch = 1      #0：充电状态；     1：不在充电
time_set = None
lat_fall = 0     #摔倒获取的经纬信息
lon_fall = 0
location2 = []
loc_get2 = []
loc_fall = ''
ai_lock = 0
#（fall_det调用）
# 2：摔倒30s拍过一次照;
# 1：摔倒10s拍过一次照；   
# 0：准备拍照；  

#获取加速度角度函数(ok)
# def get_tilt_angle(_axis):                                  
#     x = accelerometer.get_x()
#     y = accelerometer.get_y()
#     z = accelerometer.get_z()
#     if 'X' == _axis:
#         force = math.sqrt(y ** 2 + z ** 2)
#         if z < 0: return math.degrees(math.atan2(x , force))
#         else: return 180 - math.degrees(math.atan2(x , force))
#     elif 'Y' == _axis:
#         force = math.sqrt(x ** 2 + z ** 2)
#         if z < 0: return  math.degrees(math.atan2(y , force))
#         else: return 180 - math.degrees(math.atan2(y , force))
#     elif 'Z' == _axis:
#         force = math.sqrt(x ** 2 + y ** 2)
#         if (x + y) < 0: return 180 - math.degrees(math.atan2(force , z))
#         else: return math.degrees(math.atan2(force , z)) - 180
#     return 0

def make_rainbow(_neopixel, _num, _bright, _offset):          
    _rgb = ((255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,255,255), (0,0,255), (136,0,255), (255,0,0))
    for i in range(_num):
        t = 7 * i / _num
        t0 = int(t)
        r = round((_rgb[t0][0] + (t-t0)*(_rgb[t0+1][0]-_rgb[t0][0]))*_bright)>>8
        g = round((_rgb[t0][1] + (t-t0)*(_rgb[t0+1][1]-_rgb[t0][1]))*_bright)>>8
        b = round((_rgb[t0][2] + (t-t0)*(_rgb[t0+1][2]-_rgb[t0][2]))*_bright)>>8
        _neopixel[(i + _offset) % _num] = (r, g, b)


def help():
    oled.fill(0)
    oled.DispChar('我摔跤了,请帮帮我！', 15, 20)
    oled.show()


def flashlight():                                                  
    for i in range(2):
        my_rgb.fill( (255, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (255, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 255) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 255) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (255, 255, 255) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        
        
def rainbow():
    global move
    make_rainbow(my_rgb, 24, 80, move)
    my_rgb.write()
    time.sleep(1)
    move = move + 1
    
    
def common():
    oled.fill(0)
    oled.DispChar('守护者云拐杖', 24, 16)
    oled.DispChar('开', 56, 32)
    oled.show()
    #光感手电
    if light.read() < 20:
        my_rgb.fill( (255, 255, 255) )
        my_rgb.write()
    else:
        rainbow()


#心跳包发送(ok)
def heartbeat():
    data = {                #心跳包数据存储
    "uuid": uuid,
    "status":status,
    "loc": heartbeat_Loc
    }

    resp = urequests.post(url=BASE_URL+'/heartbeat', json=data)       #发送心跳包
    user_set = resp.json()
    print(user_set)
    
    

ai = NPLUS_AI()                   #小方舟初始化
ai.mode_change(1)
uart1 = machine.UART(1, baudrate=9600, tx=Pin.P14, rx=Pin.P11)
# uart2 = machine.UART(2, baudrate=9600, tx=Pin.P16, rx=Pin.P15)
while True:
#     if switch == 0:
#         my_rgb.fill( (0, 0, 0) )
#         my_rgb.write()
#         oled.fill(0)
#         oled.show()
#         if button_b.was_pressed():      #记录初始位置
#             while True:
#                 time.sleep(0.1)
#                 loc_get1 = uart1.readline()              #先读取串口一行数据
#                 if 'GNGLL' in loc_get1:
#                     location1 = (str(loc_get1).split(','))
#                     if location1[2] == 'N':
#                         lat_first = float(location1[1]) * 0.01
#                     elif location1[2] == 'S':
#                         lat_first = float(location1[1]) * 0.01 * -1
#                     else:
#                         lat_first = 0

#                     if location1[4] == 'E':
#                         lon_first = float(location1[3]) * 0.01
#                     elif location1[4] == 'W':
#                         lon_first = float(location1[3]) * 0.01 * -1
#                     else:
#                         lon_first = 0
#                     des_loc = str(lat_first) + ',' + str(lon_first)
#                     switch = 1             
#                     break

#     if switch == 1:
#         common()
#         fall_det()
#         tim1.init(period=5000, mode=Timer.PERIODIC, callback=heartbeat)
#         get_u_home()

#获得settingdata拐杖状态
    s = urequests.get(url=BASE_URL+'/get_settings/'+uuid)
    user_set = s.json()
    if user_set['code'] == 0:
        oled.DispChar('获取账户连接成功', 0, 0)
        oled.show()
        time.sleep(1)
    while True:
        if time_set == None:
            time_set = time.time()
            
        z = accelerometer.get_z()
        if not (z > -2 and z < -0.6):
            down = 1
        else:
            down = 0
            

        if down == 1:
            ai.picture_capture(0)                 #AI拐杖记录仪拍照
            if time_on == None:
                time_on = time.time()                 #记录初始时间，计时10s，10s拐杖还没起来表示老人摔倒
            my_rgb.fill( (255, 0, 0) )                #10s内先亮红灯
            my_rgb.write()
            #10s内没起来
            if time.time() - time_on > 5 and time.time() - time_on <= 30:
                if ai_lock == 0:
                    ai.picture_capture(0)
                    time.sleep_ms(100)
                    ai.picture_capture(0)
                    time.sleep_ms(100)
                    ai.picture_capture(0)
                ai_lock = 1
                fall = 1
    
    
            #30s内没起来
            if time.time() - time_on > 30:
                if ai_lock == 1:
                    ai.picture_capture(0)
                    time.sleep_ms(100)
                    ai.picture_capture(0)
                    time.sleep_ms(100)
                    ai.picture_capture(0)
                ai_lock = 2
                fall = 2
        elif down == 0:
            fall = 0
            
            
        if fall == 1:
            # while True:
            #     time.sleep(0.1)
            #     loc_get2 = uart1.readline()
            #     if 'GNGLL' in loc_get2:
            #         location2 = (str(loc_get2).split(','))
            #         if location2[2] == 'N':
            #             lat_fall = float(location2[1]) * 0.01
            #         elif location2[2] == 'S':
            #             lat_fall = float(location2[1]) * 0.01 * -1
            #         else:
            #             lat_fall = 0
    
    
            #         if location2[4] == 'E':
            #             lon_fall = float(location2[3]) * 0.01
            #         elif location2[4] == 'W':
            #             lon_fall = float(location2[3]) * 0.01 * -1
            #         else:
            #             lon_fall = 0
    
            #         break
    
            loc_fall = {"latitude":22.57149,               #修改心跳包状态
                        "longitude":114.1023}
            status = 'emergency'
            heartbeat_Loc = loc_fall
            
            flashlight()
            help()
            music.play(music.POWER_UP, wait=False, loop=True)   #示警鸣笛声
    
        if fall == 2:
            loc_fall = {"latitude":22.57149,               #修改心跳包状态
                        "longitude":114.1023}
            status = 'emergency'
            heartbeat_Loc = loc_fall
            flashlight()
            help()
            music.play(music.POWER_UP, wait=False, loop=True)
            # uart2.write('AT+SETVOLTE=1')
            # uart2.write('ATD' + str(user_set.get('settings').get('phone')))         #倒地30s后SIM模块拨打setting中紧急联系人电话                                                     #拨打电话（SIM卡）          
    
        if fall == 0:
            music.stop()
            common()
            status = "ok"
            heartbeat_Loc = None
            
        if time.time() - time_set >= 5:
            heartbeat()
            time_set = None
        
