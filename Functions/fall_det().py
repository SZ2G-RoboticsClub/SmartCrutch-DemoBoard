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
#p15：灯带2（灯数：63）


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
p0 = MPythonPin(0, PinMode.ANALOG)
my_rgb1 = neopixel.NeoPixel(Pin(Pin.P13), n=63, bpp=3, timing=1)
my_rgb2 = neopixel.NeoPixel(Pin(Pin.P15), n=63, bpp=3, timing=1)

#心跳包数据初始化
uuid = 'abfb6a0d'        #拐杖身份证
status = 'ok'                      #拐杖状态（"ok"/"emergency"/"error"/"offline"）
heartbeat_Loc = None             #location

# debug1
o = 0

#初始化服务器传输
BASE_URL = 'http://192.168.43.199:8000/demoboard'


#搭建WiFi，连接app用户手机数据
my_wifi = wifi()
my_wifi.connectWiFi("idk","12345678")


# #路径规划初始化
GEO_URL = 'http://restapi.amap.com/v3/geocode/geo?address='
# R_GEO_URL= 'https://restapi.amap.com/v3/geocode/regeo?output='
# NAV_URL = 'https://restapi.amap.com/v3/direction/walking?origin='
key = '10d4ac81004a9581c1d9de89eac4035b'


# api_key = 'Lcr1un815AuFGa7DZDQv1sqx'        #百度语音导航初始化
# secret_key = 'ujfZqO3mgcQZ52nXsfC9je02IiRDjaFb'
# method = ''
# nav_file = 'nav_file.mp3'


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
x = 1
switch = 0
move = 0        #彩虹灯变量
down = 0        #0：拐杖没倒；    1：拐杖倒了
fall = 0        #0：没摔倒；   1：摔倒了且已过了10s；    2：摔倒了30s
time_on = None     #摔倒初始时间
time_set = None    #心跳包发送初始时间
dial = 0         #拨号：      1：已拨号一次         0：未拨过号



oled.fill(0)
oled.DispChar('初始化完毕', 0, 0)
oled.show()


# ============ Modules ============

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
    # global freq
    oled.fill(0)
    oled.DispChar('我摔跤了,请帮帮我！', 10, 20)
    oled.show()
    # for freq in range(580, 685, 35):
    #     music.pitch(freq, 50)
    # for freq in range(685, 580, -35):
    #     music.pitch(freq, 50)
    
    # TEST4
    # for i in range(2):
    #   audio.play('alarm.mp3')
    #   time.sleep(1)
    
    # TEST5
    music.play(music.JUMP_UP, wait=True, loop=False)
    


#倒地闪红蓝白报警灯(ok)
def flashlight():
    global r1, r2, r3
    for r1 in range(2):
        my_rgb1.fill( (255, 0, 0) )
        my_rgb2.fill( (0, 0, 255) )
        my_rgb1.write()
        my_rgb2.write()
        time.sleep_ms(100)
        my_rgb1.fill( (0, 0, 0) )
        my_rgb2.fill( (0, 0, 0) )
        my_rgb1.write()
        my_rgb2.write()
        time.sleep_ms(100)

    for r2 in range(2):
        my_rgb2.fill( (255, 0, 0) )
        my_rgb1.fill( (0, 0, 255) )
        my_rgb1.write()
        my_rgb2.write()
        time.sleep_ms(100)
        my_rgb1.fill( (0, 0, 0) )
        my_rgb2.fill( (0, 0, 0) )
        my_rgb1.write()
        my_rgb2.write()
        time.sleep_ms(100)

    for r3 in range(2):
        my_rgb1.fill( (255, 255, 255) )
        my_rgb2.fill( (255, 255, 255) )
        my_rgb1.write()
        my_rgb2.write()
        time.sleep_ms(100)
        my_rgb1.fill( (0, 0, 0) )
        my_rgb2.fill( (0, 0, 0) )
        my_rgb1.write()
        my_rgb2.write()
        time.sleep_ms(100)


#平常状态之流水彩虹灯(ok)
def rainbow():
    global move
    make_rainbow(my_rgb1, 63, 80, move)
    make_rainbow(my_rgb2, 63, 80, move)
    my_rgb1.write()
    my_rgb2.write()
    # time.sleep(0.25)  
    move = move - 1


# A键开关灯
def on_button_a_pressed(_):
    global switch
    switch += 1

button_a.event_pressed = on_button_a_pressed


#平常状态(ok)
def common():
    global switch
    oled.fill(0)
    oled.DispChar('守护者云拐杖', 24, 16)
    oled.DispChar('开', 56, 32)
    oled.show()
    #光感手电
    if switch % 3 == 0:
        my_rgb2.fill((0,0,0))
        my_rgb1.fill((0,0,0))
        my_rgb1.write()
        my_rgb2.write()
    elif switch % 3 == 1:
        if p0.read_analog() < 100:
            my_rgb1.fill( (255, 255, 255) )
            my_rgb2.fill( (255, 255, 255) )
            my_rgb1.write()
            my_rgb2.write()
        elif p0.read_analog() >= 100:
            rainbow()    
    elif switch % 3 == 2:
        my_rgb1.fill( (255, 255, 255) )
        my_rgb2.fill( (255, 255, 255) )
        my_rgb1.write()
        my_rgb2.write()


# ============ Functions ============

#摔倒检测(ok)
def fall_det():
    global loc_cycle, loc_info, d, dial, loc_get1, location1, a1, a2, b1, b2, c1, c2, x, time_on, down, fall, lat_now, lon_now, status, heartbeat_Loc

    x = accelerometer.get_x()
    #拐杖倒地判定
    if x <= 0.5:            #究其根本
        down = 1
    else:
        down = 0


    if down == 1:
        if time_on == None:
            time_on = time.time()                 #记录初始时间，计时10s，10s拐杖还没起来表示老人摔倒
        
        my_rgb1.fill( (255, 0, 0) )            #10s内先亮红灯
        my_rgb2.fill( (255, 0, 0) )
        my_rgb1.write()
        my_rgb2.write()

        #10s内没起来
        if time.time() - time_on > 5 and time.time() - time_on <= 30:
            fall = 1
        #30s内没起来
        if time.time() - time_on > 30:
            fall = 2

    elif down == 0:
        fall = 0
        time_on = None


    if fall == 1:
        status = 'emergency'
        flashlight()
        help()


    if fall == 2:
        status = 'emergency'
        flashlight()
        help()
        if dial == 0:

            # TEST1
            oled.fill(0)
            oled.DispChar('已拨打电话', 0, 0)
            oled.show()
            print('已拨打电话')
            time.sleep(1)
            oled.fill(0)
            oled.show()

            # uart2.write('AT+SETVOLTE=1')
            # time.sleep(3)
            # uart2.write('ATD' + str(user_set.get('settings').get('phone')))         #倒地30s后SIM模块拨打setting中紧急联系人电话                                                     #拨打电话（SIM卡）          
            
            dial = 1

    if fall == 0:
        music.stop()
        common()
        dial = 0
        status = 'ok'



#心跳包发送(ok)
def heartbeat():
    global uuid, status, heartbeat_Loc, data, resp
    data = {                #心跳包数据存储
    "uuid": uuid,
    "status":status,
    "loc": heartbeat_Loc
    }

    resp = urequests.post(url=BASE_URL+'/heartbeat', json=data)       #发送心跳包

    resp = resp.json()




# ============ Main ============


audio.player_init(i2c)
audio.set_volume(100)
# uart1 = machine.UART(1, baudrate=9600, tx=Pin.P11, rx=Pin.P14)
# uart2 = machine.UART(2, baudrate=9600, tx=Pin.P15, rx=Pin.P16)

#获得settingdata拐杖状态
s = urequests.get(url=BASE_URL+'/get_settings/'+uuid)
user_set = s.json()
if user_set.get('code') == 0:
    oled.DispChar('获取账户连接成功', 0, 0)
    oled.show()
    time.sleep(1)
    oled.fill(0)
    oled.show()
    
    #家庭住址经纬度获取
    home = user_set.get('settings').get('home')
    h = urequests.get(url=GEO_URL+home+'&output=json&key='+key)
    h = h.json()
    
    # debug2
    # print(GEO_URL+home+'&output=json&key='+key)
    # print(h)
    
    home_loc = h.get('geocodes')[0].get('location')
    oled.DispChar('家庭位置记录完毕', 0, 16)
    oled.DispChar(home_loc, 0, 32)
    oled.show()
    time.sleep(1)
    oled.fill(0)
    oled.show()

    while True:
        x = accelerometer.get_x()
        # print(x)
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

        # TEST2(教科院)
        lon_now = 114.095582
        lat_now = 22.565531

        loc_cycle = str(lon_now) + ',' + str(lat_now)

        heartbeat_Loc = {
            "latitude":lat_now,
            "longitude":lon_now
            }

        if time_set == None:
            time_set = time.time()
            
        fall_det()

        if time.time() - time_set >= 5:
            heartbeat()
            time_set = None
            if resp.get('code') == 0:                   #返回数据类型正常
                continue
            elif resp.get('code') == 1:
                print('拐杖未注册')
            else:
                oled.fill(0)
                oled.DispChar('心跳包错误', 0, 0, 1)
                oled.show()

                # TEST3
                # print(resp.get('msg'))

                # time.sleep(1)
                # oled.fill(0)
                # oled.DispChar(str(resp.get('msg')), 0, 0, 1, True) #查看是否正常回应
                # oled.show()
        
else:
    # print('账户连接失败，请重新启动')
    oled.fill(0)
    oled.DispChar('账户连接失败，请重新启动', 0, 0, 1, True)
    oled.show()


#状态：倒地，common()，导航