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
#p16tx&p15rx：串口uart2(SIM卡模块)
#p11tx&p14rx：串口uart1(北斗定位模块)——测试用的是北斗，北斗只输入14tx引脚不输出
#p0: "带我回家"按钮
#p13：灯带


#摔倒判断：
# z轴加速度是否大于-0.6（垂直于屏幕向上为正方向）


#位置获取：
# a: list
# b, c: float
# a1b1c1为纬度数据，a2b2c2为经度数据

# 实时定位位置：loc_get1, location1, a/b/c:1&2


p0 = MPythonPin(0, PinMode.IN)
my_rgb = neopixel.NeoPixel(Pin(Pin.P13), n=24, bpp=3, timing=1)


#心跳包数据初始化
uuid = '3141592653589793'        #拐杖身份证
status = ''                      #拐杖状态（"ok"/"emergency"/"error"/"offline"）
heartbeat_Loc = None             #location

# heartbeat_time = None
# falltime_lock = 0                #记录时间      1：已记录一次      0：未记录过
# date_list = []
# time_list = []
# f_date = ''
# f_time = ''



#初始化服务器传输
BASE_URL = 'http://39.103.138.199:5283/demoboard'


#搭建WiFi，连接app用户手机数据
my_wifi = wifi()
my_wifi.connectWiFi("QFCS-MI","999999999")


#路径规划初始化
GEO_URL = 'http://api.map.baidu.com/geocoding/v3/?address='
R_GEO_URL= 'http://api.map.baidu.com/reverse_geocoding/v3/?'
MAP_URL = 'http://api.map.baidu.com/directionlite/v1/walking?'
ak = 'CZHBGZ6TXADxI2UecA1xfpq2GtKLMYam'


api_key = 'Lcr1un815AuFGa7DZDQv1sqx'        #百度语音导航初始化
secret_key = 'ujfZqO3mgcQZ52nXsfC9je02IiRDjaFb'
method = ''
nav_file = 'nav_file.mp3'


lat_home = 0     #家庭住址经纬信息
lon_home = 0
home_loc = ''

backhome = 0
ori_loc = ''
para1 = ''


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
    global freq
    oled.fill(0)
    oled.DispChar('我摔跤了,请帮帮我！', 15, 20)
    oled.show()
    for freq in range(880, 1930, 35):
        music.pitch(freq, 50)
    for freq in range(1930, 880, -35):
        music.pitch(freq, 50)

#倒地闪红蓝白报警灯(ok)
def flashlight():
    global i
    for i in range(2):
        my_rgb.fill( (255, 0, 0) )
        my_rgb.write()
        time.sleep_ms(100)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(100)
        my_rgb.fill( (255, 0, 0) )
        my_rgb.write()
        time.sleep_ms(100)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(100)
        my_rgb.fill( (0, 0, 255) )
        my_rgb.write()
        time.sleep_ms(100)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(100)
        my_rgb.fill( (0, 0, 255) )
        my_rgb.write()
        time.sleep_ms(100)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(100)
        my_rgb.fill( (255, 255, 255) )
        my_rgb.write()
        time.sleep_ms(100)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(100)


#平常状态之流水彩虹灯(ok)
def rainbow():
    global move
    make_rainbow(my_rgb, 24, 80, move)
    my_rgb.write()
    # time.sleep(0.25)  
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




# ============ Functions ============

#摔倒检测(ok)
def fall_det():
    global loc_cycle, loc_info, d, dial, loc_get1, location1, a1, a2, b1, b2, c1, c2, a, b, z, time_on, down, fall, lat_now, lon_now, status, heartbeat_Loc, date_list, time_list, f_time, f_date
    
    z = accelerometer.get_z()
    #拐杖倒地判定
    if z >= -0.6:            #究其根本
        down = 1
    else:
        down = 0


    if down == 1:
        if time_on == None:
            time_on = time.time()                 #记录初始时间，计时10s，10s拐杖还没起来表示老人摔倒
        my_rgb.fill( (255, 0, 0) )            #10s内先亮红灯
        my_rgb.write()
        #10s内没起来
        if time.time() - time_on > 10 and time.time() - time_on <= 30:
            fall = 1
        #30s内没起来
        if time.time() - time_on > 30:
            fall = 2
    elif down == 0:
        fall = 0


    if fall == 1:
        status = 'emergency'
        flashlight()
        help()


    if fall == 2:
        status = 'emergency'
        flashlight()
        help()
        if dial == 0:
            uart2.write('AT+SETVOLTE=1')
            uart2.write('ATD' + str(user_set.get('settings').get('phone')))         #倒地30s后SIM模块拨打setting中紧急联系人电话                                                     #拨打电话（SIM卡）          
            dial = 1

    if fall == 0:
        music.stop()
        common()
        dial = 0
        status = 'ok'



#"带你回家"
def take_u_home():
    global loc_cycle, method, _dat, _f, para1, nav, route, ak, MAP_URL, lat_now, lon_now, ori_loc, data_audio, nav_file, r_audio 
    
    if p0.read_digital() == 1:
        backhome = backhome + 1
    
    if backhome == 0:
        fall_det()
    elif backhome != 0:
        fall_det()
        ori_loc = str(lat_now) + ',' + str(lon_now)
        # oled.fill(0)
        # oled.DispChar('当前位置记录完毕', 0, 16)
        # oled.DispChar(ori_loc, 0, 32)
        # oled.show()
        # time.sleep(3)
        # oled.fill(0)
        # oled.show()
        # print(ori_loc)
        para1 = 'origin='+ori_loc+'&destination='+home_loc+'&ak='+ak
        # print(para1)
        nav = urequests.get(url=MAP_URL+str(para1))
        # print(nav)
        route = nav.json()
        # print(route)
        if route.get('status') == 0:
            # oled.fill(0)
            # oled.DispChar(str(route), 0, 0, 1, True)
            # oled.show()
            # time.sleep(5)
            # oled.fill(0)
            # oled.show()
            method = route.get('result').get('routes')[0].get('steps')[0].get('instruction').replace('<b>','').replace('</b>','')
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
        elif route.get('status') != 0:
            # oled.fill(0)
            # oled.DispChar(str(route), 0, 0, 1, True)
            # oled.show()
            # time.sleep(5)
            # oled.fill(0)
            # oled.DispChar('导航结束！', 0, 0)
            # oled.show()
            # time.sleep(2)
            # oled.fill(0)
            # oled.show()
            audio.play('nav_end.mp3')
            time.sleep(3)
            
            backhome = 0
                # break
            


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

# ai = NPLUS_AI()
# ai.mode_change(1)
audio.player_init(i2c)
audio.set_volume(100)
uart1 = machine.UART(1, baudrate=9600, tx=Pin.P11, rx=Pin.P14)
uart2 = machine.UART(2, baudrate=9600, tx=Pin.P16, rx=Pin.P15)

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
    h = urequests.get(url=GEO_URL+home+'&output=json&ak='+ak)
    h = h.json()
    lat_home = h.get('result').get('location').get('lat')
    lon_home = h.get('result').get('location').get('lng')
    home_loc = str(lat_home) + ',' + str(lon_home)
    oled.DispChar('家庭位置记录完毕', 0, 16)
    oled.DispChar(home_loc, 0, 32)
    oled.show()
    time.sleep(1)
    oled.fill(0)
    oled.show()

    while True:
        loc_get1 = uart1.readline()
        location1 = (str(loc_get1).split(','))
        if location1[2] == 'N':
            a1 = list(str(location1[1]))
            b1 = float(''.join(a1[2:]))
            c1 = ((100 - 0) / (60 - 0)) * (b1 - 0) + 0
            lat_now = math.floor(float(location1[1]) * 0.01) + c1 * 0.01
        elif location1[2] == 'S':
            a1 = list(str(location1[1]))
            b1 = float(''.join(a1[2:]))
            c1 = ((100 - 0) / (60 - 0)) * (b1 - 0) + 0
            lat_now = math.floor(float(location1[1]) * 0.01 * -1) + c1 * 0.01
        else:
            lat_now = 0


        if location1[4] == 'E':
            a2 = list(str(location1[3]))
            b2 = float(''.join(a2[3:]))
            c2 = ((100 - 0) / (60 - 0)) * (b2 - 0) + 0
            lon_now = math.floor(float(location1[3]) * 0.01) + c2 * 0.01
        elif location1[4] == 'W':
            a2 = list(str(location1[3]))
            b2 = float(''.join(a2[3:]))
            c2 = ((100 - 0) / (60 - 0)) * (b2 - 0) + 0
            lon_now = math.floor(float(location1[3]) * 0.01 * -1) + c2 * 0.01
        else:
            lon_now = 0

        loc_cycle = lat_now + ',' + lon_now
        d = urequests.post(url=R_GEO_URL+'ak='+ak+'&output=json&coordtype=wgs84ll&location='+loc_cycle)
        d = d.json()
        loc_info = d.get('result').get('formatted_address')

        heartbeat_Loc = {
            "latitude":lat_now,
            "longitude":lon_now,
            "info": loc_info
            }

        if time_set == None:
            time_set = time.time()

        take_u_home()

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
                oled.DispChar(str(resp.get('msg')), 0, 16, 1, True) #查看是否正常回应
                oled.show()
        
else:
    # print('账户连接失败，请重新启动')
    oled.fill(0)
    oled.DispChar('账户连接失败，请重新启动', 0, 0, 1, True)
    oled.show()


#状态：倒地，充电，common()，导航