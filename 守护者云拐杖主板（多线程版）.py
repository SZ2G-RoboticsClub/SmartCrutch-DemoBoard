from machine import Timer
from machine import UART
from mpython import *
from bluebit import *
from nplus.ai import *
import math
import music
import neopixel
import _thread
import sys
import time
import socket   #urequests

#p5：MP3模块
#p1&p6：串口uart1
#p0&p3：串口uart2
#p2：“记录”按钮
#p14 灯带1
#p15：灯带2
#p16：“回家”按钮
#摔倒判断：角度

my_rgb1 = neopixel.NeoPixel(Pin(Pin.P15), n=21, bpp=3, timing=1)#引脚设定
my_rgb2 = neopixel.NeoPixel(Pin(Pin.P14), n=21, bpp=3, timing=1)
mp3 = MP3(Pin.P5)
p1 = MPythonPin(1, PinMode.ANALOG)
p2 = MPythonPin(2, PinMode.IN)
p16 = MPythonPin(16, PinMode.IN)

#初始化服务器传输
host = "192.168.1.105"
port = 54269
my_wifi = wifi()         #搭建WiFi，连接app用户手机数据
mywifi.connectWiFi("QFCS1","12345678")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)           
s.connect(host,port)                                            

backhome = 0
move = 0
timestart = 0
fall = 0
down = 0
location = []
latitude_first = 0
longtitude_first = 0
latitude_now = 0
longtitude_now = 0
ai = NPLUS_AI()
tim1 = Timer(1)
#获取一次app上的电话（app上标注重启拐杖即生效）
phone = conn.recv(1024)                               #获取紧急联系人电话
phone = phone.decode('utf-8')                         #以utf-8编码解码字符串
mp3.volume = 30
uart1 = machine.UART(1, baudrate=115200, tx=Pin.P1, rx=Pin.P6)
uart2 = machine.UART(2, baudrate=115200, tx=Pin.P0, rx=Pin.P3)

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
        if _Az < 0: return  math.degrees(math.atan2(y , force))
        else: return 180 - math.degrees(math.atan2(y , force))
    elif 'Z' == _axis:
        force = math.sqrt(x ** 2 + y ** 2)
        if (x + y) < 0: return 180 - math.degrees(math.atan2(force , z))
        else: return math.degrees(math.atan2(force , z)) - 180
    return 0

def help():                                                   #呼叫路人来帮忙(ok)
    oled.fill(0)
    oled.DispChar('我摔跤了,请帮帮我！', 15, 20)
    oled.show()
    music.play(music.POWER_UP, wait=False, loop=True)

def light():                                                  #倒地闪红蓝报警灯(ok)
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

def common():                                                 #平常状态(ok)
    oled.fill(0)
    oled.DispChar('智能云拐杖', 24, 16)
    oled.DispChar('开', 56, 32)
    oled.show()
    #光感手电
    if light.read() < 25:                          #测试数值0-4095
        my_rgb1.fill( (255, 255, 255) )
        my_rgb2.fill( (255, 255, 255) )
        my_rgb1.write()
        my_rgb2.write()
    else:
        liushuideng()
       
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
    make_rainbow(my_rgb1, 23, 80, move)
    make_rainbow(my_rgb2, 23, 80, move)
    my_rgb1.write()
    my_rgb2.write()
    time.sleep(0.25)
    move = move + 1



def loc_get():                        #线程1：北斗地址获取
    while True:
        if uart1.read():                  
                location = list(uart1.readline())
def fall_down():                      #线程2：判断跌倒
    while True:
        common()
        if get_tilt_angle('X') <= 15 or get_tilt_angle('X') >= 165 or get_tilt_angle('Y') <= 110 or get_tilt_angle('Y') >= 250 or get_tilt_angle('Z') <= -170 or get_tilt_angle('Z') >= -20:
            down = 1
        else:
            down = 0
        
        if down == 1:
            ai.video_capture(60)                 #AI拐杖记录仪
            timestart = time.ticks_ms()          #计时10s，10s内灯带先变红
            my_rgb1.brightness(100 / 100)
            my_rgb2.brightness(100 / 100)
            my_rgb1.fill( (255, 0, 0) )
            my_rgb2.fill( (255, 0, 0) )
            my_rgb1.write()
            my_rgb2.write()
            #10s内没起来
            if time.ticks_ms() - timestart > 10000:
                fall = 1
            #30s内没起来
            if time.ticks_ms() - timestart >= 30000:
                fall = 2
        elif down == 0:
            fall = 0
            timestart = 0
        
        if fall == 1:
            s.send(location)                      #发送定位到app并发警报声
            light()
            help()
        elif fall == 2:
            light()
            sound()
            uart2.write(('ATD' + str(phone)))     #拨打电话（SIM卡）
            help()
        elif fall == 0:
            common()
            music.stop()
def get_u_home():                           #线程3：带你回家
    while True:
        common()
        
        if p16.read_digital() == 1:              #防止老人按很多次
            backhome = 1
        if :               #出门抬起拐杖
            backhome = -1
        
        if backhome == -1:                    #出门抬起拐杖，北斗记录初始位置
            latitude_first = str(float(location[20:29]) * 0.01 + location[20])      #存取初始纬度
            longtitude_first = str(float(location[32:42]) * 0.01 + location[43])    #存取初始经度
            #n为时间与字符间空格数(为2)
        if backhome == 1:                    #按一下“回家”按钮，北斗记录当前位置并导航语音带老人回初始位置
            latitude_now = str(float(location[20:29]) * 0.01 + location[18+n])      #存取当前纬度
            longtitude_now = str(float(location[32:42]) * 0.01 + location[43])      #存取当前经度
            #语音导航带老人回家
            backhome = 0 #导航到家


_thread.start_new_thread(fall_down,())
_thread.start_new_thread(loc_get,())
_thread.start_new_thread(get_u_home,())