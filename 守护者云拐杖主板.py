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


#引脚：
#p16tx&p15rx：串口uart2(SIM卡模块)
#p11tx&p14rx：串口uart1(北斗定位模块)——测试用的是北斗，北斗只输入14tx引脚不输出
#p0&p1：小方舟模块
#p13：灯带
#掌控板a键：“带我回家”按钮
#掌控板b键：记录初始位置

#摔倒判断：z轴加速度

#位置获取：
# a: list
# b, c: float
# 奇数为纬度数据，偶数为经度数据

#出门初始位置：loc_get1, location1, a/b/c:1&2
#摔倒位置：loc_get2, location2, a/b/c:3&4
#想回家时位置：loc_get3, location3, a/b/c:5&6


my_rgb = neopixel.NeoPixel(Pin(Pin.P13), n=24, bpp=3, timing=1)


#心跳包数据初始化
uuid = '3141592653589793'        #拐杖身份证
status = ""                      #拐杖状态（"ok"/"emergency"/"error"/"offline"）
heartbeat_Loc = None             #location


#初始化服务器传输
BASE_URL = 'http://192.168.31.125:8000/demoboard'
my_wifi = wifi()         #搭建WiFi，连接app用户手机数据
my_wifi.connectWiFi("QFCS-MI","999999999")


#路径规划初始化
MAP_URL = 'http://api.map.baidu.com/directionlite/v1/walking?'
ak = 'CZHBGZ6TXADxI2UecA1xfpq2GtKLMYam'

lat_first = 0     #出门获取经纬信息
lon_first = 0
location1 = []
a7 = []
a8 = []
b7 = 0
b8 = 0
c7 = 0
c8 = 0
des_loc = ''

lat_now = 0       #按下带我回家按钮记录的经纬信息
lon_now = 0
location3 = []
a5 = []
a6 = []
b5 = 0
b6 = 0
c5 = 0
c6 = 0
ori_loc = ''
para1 = ''



#全局变量定义                                            
backhome = 0    #1：按下带我回家按钮；   0：导航到家或空状态
move = 0        #彩虹灯变量
down = 0        #0：拐杖没倒；    1：拐杖倒了
fall = 0        #0：没摔倒；   1：摔倒了且已过了10s；    2：摔倒了30s
time_on = None     #摔倒初始时间
time_set = None    #心跳包发送初始时间
switch = 1      #0：充电状态；     1：不在充电——检测摔倒或导航
lat_fall = 0     #摔倒获取的经纬信息
lon_fall = 0
location2 = []
a1 = []
a2 = []
b1 = 0
b2 = 0
c1 = 0
c2 = 0
loc_fall = ''
ai_lock = 0
#（fall_det调用）
# 2：摔倒30s拍过一次照;
# 1：摔倒10s拍过一次照；   
# 0：准备拍照；   

oled.DispChar('初始化完毕', 0, 0)
oled.show()


# ============ Module ============

#平常状态之彩虹灯效设定(ok)
def make_rainbow(_neopixel, _num, _bright, _offset):          
    _rgb = ((255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,255,255), (0,0,255), (136,0,255), (255,0,0))
    for i in range(_num):
        t = 7 * i / _num
        t0 = int(t)
        r = round((_rgb[t0][0] + (t-t0)*(_rgb[t0+1][0]-_rgb[t0][0]))*_bright)>>8
        g = round((_rgb[t0][1] + (t-t0)*(_rgb[t0+1][1]-_rgb[t0][1]))*_bright)>>8
        b = round((_rgb[t0][2] + (t-t0)*(_rgb[t0+1][2]-_rgb[t0][2]))*_bright)>>8
        _neopixel[(i + _offset) % _num] = (r, g, b)


#呼叫路人来帮忙(ok)
def help():
    oled.fill(0)
    oled.DispChar('我摔跤了,请帮帮我！', 15, 20)
    oled.show()
    music.play(music.POWER_UP, wait=True, loop=False)


#倒地闪红蓝白报警灯(ok)
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


#平常状态之流水彩虹灯(ok)
def rainbow():
    global move
    make_rainbow(my_rgb, 23, 80, move)
    my_rgb.write()
    time.sleep(0.25)
    move = move + 1


#平常状态(ok)
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



# ============ Function ============

#摔倒检测(ok)
def fall_det():
    global time_on, ai_lock, switch, fall, lat_first, lon_first, lat_fall, lon_fall, loc_fall, status, heartbeat_Loc, des_loc
    z = accelerometer.get_z()
    #拐杖倒地判定
    if z > 0 or z <= 0 and z >= -0.6:            #究其根本
        down = 1
    else:
        down = 0


    if down == 1:
        ai.picture_capture(0)                 #AI拐杖记录仪拍照
        if time_on == None:
            time_on = time.time()                 #记录初始时间，计时10s，10s拐杖还没起来表示老人摔倒
        my_rgb.fill( (255, 0, 0) )            #10s内先亮红灯
        my_rgb.write()
        #10s内没起来
        if time.time() - time_on > 10 and time.time() - time_on <= 30:
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
        # loc_get2 = uart1.readline()
        # while True:
        #     location2 = (str(loc_get2).split(','))
        #     if location2[2] == 'N':
        #         a3 = list(str(location2[1]))
        #         b3 = float(''.join(a3[2:]))
        #         c3 = ((100 - 0) / (60 - 0)) * (b3 - 0) + 0
        #         lat_fall = math.floor(float(location2[1]) * 0.01) + c3 * 0.01
        #     elif location2[2] == 'S':
        #         a3 = list(str(location2[1]))
        #         b3 = float(''.join(a3[2:]))
        #         c3 = ((100 - 0) / (60 - 0)) * (b3 - 0) + 0
        #         lat_fall = math.floor(float(location2[1]) * 0.01 * -1) + c3 * 0.01
        #     else:
        #         lat_fall = 0


        #     if location2[4] == 'E':
        #         a4 = list(str(location2[3]))
        #         b4 = float(''.join(a4[3:]))
        #         c4 = ((100 - 0) / (60 - 0)) * (b4 - 0) + 0
        #         lon_fall = math.floor(float(location2[3]) * 0.01) + c4 * 0.01
        #     elif location2[4] == 'W':
        #         a4 = list(str(location2[3]))
        #         b4 = float(''.join(a4[3:]))
        #         c4 = ((100 - 0) / (60 - 0)) * (b4 - 0) + 0
        #         lon_fall = math.floor(float(location2[3]) * 0.01 * -1) + c4 * 0.01
        #     else:
        #         lon_fall = 0

        #     break

        # loc_fall = {"latitude":lat_fall,               #修改心跳包状态
        #             "longitude":lon_fall}
        # status = 'emergency'
        # heartbeat_Loc = loc_fall
        
        flashlight()
        music.play(music.POWER_UP, wait=True, loop=False)   #示警鸣笛声

    if fall == 2:
        # loc_fall = {"latitude":lat_fall,               #修改心跳包状态
        #             "longitude":lon_fall}
        # status = 'emergency'
        # heartbeat_Loc = loc_fall

        flashlight()
        music.play(music.POWER_UP, wait=True, loop=False)
        # uart2.write('AT+SETVOLTE=1')
        # uart2.write('ATD' + str(user_set.get('settings').get('phone')))         #倒地30s后SIM模块拨打setting中紧急联系人电话                                                     #拨打电话（SIM卡）          

    if fall == 0:
        music.stop()
        common()
        status = "ok"
        heartbeat_Loc = None


#"带你回家"
def get_u_home():
    global end_way, i, route, home_lock, backhome, ak, MAP_URL, lat_now, lon_now, home_lock, loc_get3, location3, ori_loc, des_loc, parameters
    if button_a.was_pressed():
        while True:
            loc_get3 = uart1.readline()
            location3 = (str(loc_get3).split(','))
            if location3[2] == 'N':
                a5 = list(str(location3[1]))
                b5 = float(''.join(a5[2:]))
                c5 = ((100 - 0) / (60 - 0)) * (b5 - 0) + 0
                lat_now = math.floor(float(location3[1]) * 0.01) + c5 * 0.01
            elif location3[2] == 'S':
                a5 = list(str(location3[1]))
                b5 = float(''.join(a5[2:]))
                c5 = ((100 - 0) / (60 - 0)) * (b5 - 0) + 0
                lat_now = math.floor(float(location3[1]) * 0.01 * -1) + c5 * 0.01
            else:
                lat_now = 0
            
            #经度存取，东正西负，否则0°
            if location3[4] == 'E':
                a6 = list(str(location3[3]))
                b6 = float(''.join(a6[3:]))
                c6 = ((100 - 0) / (60 - 0)) * (b6 - 0) + 0
                lon_now = math.floor(float(location3[3]) * 0.01) + c6 * 0.01
            elif location3[4] == 'W':
                a6 = list(str(location3[3]))
                b6 = float(''.join(a6[3:]))
                c6 = ((100 - 0) / (60 - 0)) * (b6 - 0) + 0
                lon_now = math.floor(float(location3[3]) * 0.01 * -1) + c6 * 0.01
            else:
                lon_now = 0
                
            ori_loc = str(lat_now) + ',' + str(lon_now)
            
            # oled.fill(0)
            # oled.DispChar('当前位置记录完毕', 0, 16)
            # oled.DispChar(ori_loc, 0, 32)
            # oled.show()
            # time.sleep(1)
            # oled.fill(0)
            # oled.show()
            # print(ori_loc)
            para1 = 'origin='+ori_loc+'&destination='+des_loc+'&ak='+ak
            # print(para1)
            nav = urequests.get(url=MAP_URL+str(para1))
            # print(nav)
            route = nav.json()
            # print(route)
            if route.get('status') == 0:
                method = route.get('result').get('routes')[0].get('steps')[0].get('instruction')
                oled.fill(0)
                oled.DispChar(method, 0, 0, 1, True)
                oled.show()
            elif route.get('status') != 0:
                oled.fill(0)
                oled.DispChar('导航结束！', 0, 0)
                oled.show()
                time.sleep(2)
                oled.fill(0)
                oled.show()
                break

        backhome = 0        #导航到家
        


#心跳包发送(ok)
def heartbeat():
    global uuid, status, heartbeat_Loc
    data = {                #心跳包数据存储
    "uuid": uuid,
    "status":status,
    "loc": heartbeat_Loc
    }

    resp = urequests.post(url=BASE_URL+'/heartbeat', json=data)       #发送心跳包

    resp = resp.json()
    

    # if user_set['code'] == 0:                   #返回数据类型正常
    #     continue
    # elif user_set['code'] == 1:
    #     print('拐杖未注册')
    # else:
    #     print(user_set.get('msg'))          #查看是否正常回应


ai = NPLUS_AI()
ai.mode_change(1)
uart1 = machine.UART(1, baudrate=9600, tx=Pin.P11, rx=Pin.P14)
uart2 = machine.UART(2, baudrate=9600, tx=Pin.P16, rx=Pin.P15)

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
            
    
    if switch == 0:
        if button_b.was_pressed():      #记录初始位置
            loc_get1 = uart1.readline()
            while True:
                location1 = (str(loc_get1).split(','))
                if location1[2] == 'N':
                    a7 = list(str(location1[1]))
                    b7 = float(''.join(a7[2:]))
                    c7 = ((100 - 0) / (60 - 0)) * (b7 - 0) + 0
                    lat_first = math.floor(float(location1[1]) * 0.01) + c7 * 0.01
                elif location1[2] == 'S':
                    a7 = list(str(location1[1]))
                    b7 = float(''.join(a7[2:]))
                    c7 = ((100 - 0) / (60 - 0)) * (b7 - 0) + 0
                    lat_first = math.floor(float(location1[1]) * 0.01 * -1) + c7 * 0.01
                else:
                    lat_first = 0

                if location1[4] == 'E':
                    a8 = list(str(location1[3]))
                    b8 = float(''.join(a8[3:]))
                    c8 = ((100 - 0) / (60 - 0)) * (b8 - 0) + 0
                    lon_first = math.floor(float(location1[3]) * 0.01) + c8 * 0.01
                elif location1[4] == 'W':
                    a8 = list(str(location1[3]))
                    b8 = float(''.join(a8[3:]))
                    c8 = ((100 - 0) / (60 - 0)) * (b8 - 0) + 0
                    lon_first = math.floor(float(location1[3]) * 0.01 * -1) + c8 * 0.01
                else:
                    lon_first = 0

                des_loc = str(lat_first) + ',' + str(lon_first)
                oled.fill(0)
                oled.DispChar('初始位置记录完毕', 0, 16)
                oled.DispChar(des_loc, 0, 32)
                oled.show()
                time.sleep(1)
                oled.fill(0)
                oled.show()
                switch = 1             
                break

    if switch == 1:
        fall_det()
        get_u_home()

        
    if time.time() - time_set >= 5:
        heartbeat()
        time_set = None
        
    # if touchpad_h.is_pressed():
    #     switch = 0
    


#状态：倒地，充电，common()，导航