from machine import UART
from mpython import *
from bluebit import *
from nplus.ai import *
import math
import music
import ntptime
import neopixel
import _thread
import sys
import time
import urequests



#p16&p15：串口uart1（待测试）
#p0&p1：小方舟模块
#p13：灯带1
#p14：灯带2
#p5：“回家”按钮


#摔倒判断：角度

#小方舟学习数据：id0为充电座上的二维码

my_rgb1 = neopixel.NeoPixel(Pin(Pin.P13), n=21, bpp=3, timing=1)#引脚设定
my_rgb2 = neopixel.NeoPixel(Pin(Pin.P15), n=21, bpp=3, timing=1)
p5 = MPythonPin(5, PinMode.IN)



BASE_URL = '/demoboard'
uuid = '14159265358979313530481716qfpkydy666'


#初始化服务器传输
my_wifi = wifi()         #搭建WiFi，连接app用户手机数据
mywifi.connectWiFi("QFCS1","12345678")


                                            
backhome = 0
move = 0
fall = 0
time_on = 0
switch = 0
down = 0
location = []
lat_first = 0
lon_first = 0
lat_now = 0
lon_now = 0
loc_get = []
c_lock = 0
loc_lock = 0
ai = NPLUS_AI()
ai.mode_change(1)
tim1 = Timer(1)
uart1 = machine.UART(1, baudrate=9600, tx=Pin.P16, rx=Pin.P15)   


#Module
def get_tilt_angle(_axis):                                  
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()
    if 'X' == _axis:
        force = math.sqrt(y ** 2 + z ** 2)
        if z < 0: return math.degrees(math.atan2(x , force))
        else: return 180 - math.degrees(math.atan2(x , force))
    elif 'Y' == _axis:
        force = math.sqrt(x ** 2 + z ** 2)
        if z < 0: return  math.degrees(math.atan2(y , force))
        else: return 180 - math.degrees(math.atan2(y , force))
    elif 'Z' == _axis:
        force = math.sqrt(x ** 2 + y ** 2)
        if (x + y) < 0: return 180 - math.degrees(math.atan2(force , z))
        else: return math.degrees(math.atan2(force , z)) - 180
    return 0


def help():                                                   #呼叫路人来帮忙
    oled.fill(0)
    oled.DispChar('我摔跤了,请帮帮我！', 15, 20)
    oled.show()
    music.play(music.POWER_UP, wait=False, loop=True)


def flashlight():                                                  #倒地闪红蓝报警灯
    my_rgb1.fill( (255, 0, 0) )
    my_rgb2.fill( (255, 0, 0) )
    my_rgb1.write()
    my_rgb2.write()
    sleep_ms(50)
    my_rgb1.fill( (0, 0, 0) )
    my_rgb2.fill( (0, 0, 0) )
    my_rgb1.write()
    my_rgb2.write()
    sleep_ms(50)
    my_rgb1.fill( (255, 0, 0) )
    my_rgb2.fill( (255, 0, 0) )
    my_rgb1.write()
    my_rgb2.write()
    sleep_ms(50)
    my_rgb1.fill( (0, 0, 0) )
    my_rgb2.fill( (0, 0, 0) )
    my_rgb1.write()
    my_rgb2.write()
    sleep_ms(50)
    my_rgb1.fill( (0, 0, 255) )
    my_rgb2.fill( (0, 0, 255) )
    my_rgb1.write()
    my_rgb2.write()
    sleep_ms(50)
    my_rgb1.fill( (0, 0, 0) )
    my_rgb2.fill( (0, 0, 0) )
    my_rgb1.write()
    my_rgb2.write()
    sleep_ms(50)
    my_rgb1.fill( (0, 0, 255) )
    my_rgb2.fill( (0, 0, 255) )
    my_rgb1.write()
    my_rgb2.write()
    sleep_ms(50)
    my_rgb1.fill( (0, 0, 0) )
    my_rgb2.fill( (0, 0, 0) )
    my_rgb1.write()
    my_rgb2.write()
    sleep_ms(50)
    my_rgb1.fill( (255, 255, 255) )
    my_rgb2.fill( (255, 255, 255) )
    my_rgb1.write()
    my_rgb2.write()
    sleep_ms(50)
    my_rgb1.fill( (0, 0, 0) )
    my_rgb2.fill( (0, 0, 0) )
    my_rgb1.write()
    my_rgb2.write()
    sleep_ms(50)
    my_rgb1.fill( (255, 255, 255) )
    my_rgb2.fill( (255, 255, 255) )
    my_rgb1.write()
    my_rgb2.write()
    sleep_ms(50)
    my_rgb1.fill( (0, 0, 0) )
    my_rgb2.fill( (0, 0, 0) )
    my_rgb1.write()
    my_rgb2.write()
    sleep_ms(50)
    time.sleep(0.8)    


def make_rainbow(_neopixel, _num, _bright, _offset):          #平常状态之彩虹灯效设定(ok)
    _rgb = ((255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,255,255), (0,0,255), (136,0,255), (255,0,0))
    for i in range(_num):
        t = 7 * i / _num
        t0 = int(t)
        r = round((_rgb[t0][0] + (t-t0)*(_rgb[t0+1][0]-_rgb[t0][0]))*_bright)>>8
        g = round((_rgb[t0][1] + (t-t0)*(_rgb[t0+1][1]-_rgb[t0][1]))*_bright)>>8
        b = round((_rgb[t0][2] + (t-t0)*(_rgb[t0+1][2]-_rgb[t0][2]))*_bright)>>8
        _neopixel[(i + _offset) % _num] = (r, g, b)


def liushuideng():                                            #平常状态之流水彩虹灯(ok)
    global move
    make_rainbow(my_rgb1, 24, 80, move)
    make_rainbow(my_rgb2, 24, 80, move)
    my_rgb1.write()
    my_rgb2.write()
    time.sleep(0.25)
    move = move + 1


def common():                                                 #平常状态(ok)
    rgb.fill( (0, 0, 0) )
    rgb.write()
    time.sleep_ms(1)
    oled.fill(0)
    oled.DispChar('守护者云拐杖', 18, 16)
    oled.DispChar('开', 56, 32)
    oled.show()
    #光感手电
    if p5.read_analog() < 25:                          #测试数值0-4095
        my_rgb1.fill( (255, 255, 255) )
        my_rgb2.fill( (255, 255, 255) )
        my_rgb1.write()
        my_rgb2.write()
    else:
        liushuideng()




#Thread

def fall_det():                      
    while True:
        global lat_first, lon_first, lat_now, lon_now, loc_lock
        common()

        if ai.get_id_data(0) and c_lock != -1:               #识别到二维码，开始充电
            switch = 0
            c_lock = -1
            loc_lock = 0
            
        if not ai.get_id_data(0) and c_lock == -1:         #从充电座提起断电自动记录位置——识别二维码不在就是离开出门
            backhome = -1
            c_lock = 1
            switch = 1
            
        if backhome == -1 and c_lock == 1:      #记录初始位置
            if uart1.any() and loc_lock = 0:
                time.sleep(0.1)
                loc_get = uart1.readline()
                if 'GNGLL' in loc_get:
                    location = (str(loc_get).split(','))
                    if location[2] == 'N':
                        lat_first = float(location[1])
                    elif location[2] == 'S':
                        lat_first = float(location[1]) * -1
                    else:
                        lat_first = 0

                    if location[4] == 'E':
                        lon_first = float(location[3])
                    elif location[4] == 'W':
                        lon_first = float(location[3]) * -1
                    else:
                        lon_first = 0
                    
                    loc_lock = 1

                    c_lock = 0             #只在充电一次结束的时候记录一次经纬度

        if switch == 1:
            common()
            if get_tilt_angle('X') <= 15 or get_tilt_angle('X') >= 165 or get_tilt_angle('Y') <= 110 or get_tilt_angle('Y') >= 250 or get_tilt_angle('Z') <= -170 or get_tilt_angle('Z') >= -20:
                down = 1
            else:
                down = 0
        

            if down == 1:
                ai.video_capture(60)                 #AI拐杖记录仪
                time_on = time.time()
                my_rgb1.brightness(100 / 100)
                my_rgb2.brightness(100 / 100)
                my_rgb1.fill( (255, 0, 0) )
                my_rgb2.fill( (255, 0, 0) )
                my_rgb1.write()
                my_rgb2.write()
                #10s内没起来
                if time.time() - time_on > 10 and time.time() - time_on <= 30:
                    fall = 1
                #30s内没起来
                elif time.time() - time_on > 30:
                    fall = 2
            elif down == 0:
                fall = 0
        

            if fall == 1:
                if #导航定位
                status = "emergency"
                flashlight()
                help()
                
            elif fall == 2:
                flashlight()
                help()
                uart.write('ATD' + str(s.get('phone')))                                                                         #拨打电话（SIM卡）          
            elif fall == 0:
                common()
                music.stop()

            if p5.read_digital() == 0:
                backhome = 1

            if backhome == 1 and c_lock == 0:                                                                                      #记录当前位置
                location = list(uart1.readline())
                latitude_now = str(float(location[19:28])) * 0.01 + str(location[29])        #存取当前纬度
                longtitude_now = str(float(location[31:41])) * 0.01 + str(location[42])      #存取当前经度
                #语音导航带老人回家
                backhome = 0 #导航到家

        elif switch == 0:
            oled.fill(0)
            oled.DispChar('守护者云拐杖', 18, 16)
            oled.DispChar('充电中', 40, 32)
            oled.show()
            rgb[1] = (int(255), int(0), int(0))
            rgb.write()
            time.sleep_ms(1)


def home_thread():



def heartbeat_thread():
    while True:

        data = {
        "uuid": uuid,
        "status":status
        "loc": None
        }

        time.sleep(5)

        resp = urequests.post(url=BASE_URL+'/heartbeat/', data=data)

        if resp.code != 200:
            print('数据传输错误')
            continue

        resp = resp.json()

        if resp['code'] == 0:
            continue
        elif resp['code'] == 1:
            
        else:
            print(resp['msg'])





#获得settingdata
try:
    s = urequests.get(url=BASE_URL+'/get_settings/')
except:
    print('无法连接服务器，请重试')
else:
    _thread.start_new_thread(heartbeat_thread,())
    _thread.start_new_thread(main_thread,())

