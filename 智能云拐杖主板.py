from machine import Timer
from machine import UART
from mpython import *
from bluebit import *
from nplus.ai import *
import smartcamera
import math
import music
import neopixel
import time
import socket

#p0：MP3模块
#p1&p6：串口uart1
#p0&p3：串口uart2
#p2：“已回家”按钮
#p13：rgb灯
#p14 灯带1
#p15：灯带2
#p16：“回家”按钮
#用http传输

#song1 = “我想回家，请帮帮我！”

#摔倒判断：角度

my_rgb1 = neopixel.NeoPixel(Pin(Pin.P15), n=21, bpp=3, timing=1)#引脚设定
my_rgb2 = neopixel.NeoPixel(Pin(Pin.P14), n=21, bpp=3, timing=1)
mp3 = MP3(Pin.P0)
p13 = MPythonPin(13, PinMode.OUT)
p1 = MPythonPin(1, PinMode.ANALOG)
p2 = MPythonPin(2, PinMode.IN)
p16 = MPythonPin(16, PinMode.IN)

#初始化服务器传输
host = 192.168.1.105
port = 54269
my_wifi = wifi()         #搭建WiFi，连接app用户手机数据
mywifi.connectWiFi("","")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                                                                 # 创建TCP的套接字,也可以不给定参数。默认为TCP通讯方式
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                                                                             # 设置socket属性
s.connect((host,port))                                                                                                            # 设置要连接的服务器端的IP和端口,并连接

def get_tilt_angle(_axis):                                  
    _Ax = accelerometer.get_x()
    _Ay = accelerometer.get_y()
    _Az = accelerometer.get_z()
    if 'X' == _axis:
        _T = math.sqrt(_Ay ** 2 + _Az ** 2)
        if _Az < 0: return math.degrees(math.atan2(_Ax , _T))
        else: return 180 - math.degrees(math.atan2(_Ax , _T))
    elif 'Y' == _axis:
        _T = math.sqrt(_Ax ** 2 + _Az ** 2)
        if _Az < 0: return  math.degrees(math.atan2(_Ay , _T))
        else: return 180 - math.degrees(math.atan2(_Ay , _T))
    elif 'Z' == _axis:
        _T = math.sqrt(_Ax ** 2 + _Ay ** 2)
        if (_Ax + _Ay) < 0: return 180 - math.degrees(math.atan2(_T , _Az))
        else: return math.degrees(math.atan2(_T , _Az)) - 180
    return 0

def help():                                                   #呼叫路人来帮忙(ok)
    oled.fill(0)
    oled.DispChar('我摔跤了,请帮帮我！', 15, 20)
    oled.show()
    sound()
    pass

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

def sound():                                                  #MP3发警报声(ok)
    music.play(music.POWER_UP, wait=False, loop=True)

def common():                                                 #平常状态(ok)
    oled.fill(0)
    oled.DispChar('智能云拐杖', 24, 16)
    oled.DispChar('开', 56, 32)
    oled.show()
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

def home():                                                   #“回家”住址自动换行显示(ok)
    if len(dizhi) < 10:
        oled.fill(0)
        oled.DispChar('住址：', 0, 0, 0)
        oled.DispChar(dizhi[0:], 0, 16, 1)
        oled.show()
    if len(dizhi) >= 10 and len(dizhi) < 20:
        oled.fill(0)
        oled.DispChar('住址：', 0, 0, 0)
        oled.DispChar(dizhi[0:10], 0, 16, 1)
        oled.DispChar(dizhi[10:], 0, 32, 1)
        oled.show()
    if len(dizhi) >= 20:
        oled.fill(0)
        oled.DispChar('住址：', 0, 0, 0)
        oled.DispChar(dizhi[0:10], 0, 16, 1)
        oled.DispChar(dizhi[10:20], 0, 32, 1)
        oled.DispChar(dizhi[20:], 0, 48, 1)
        oled.show()
                       #app上地址要小于30个字



backhome = 0
move = 0
timestart = 0
fall = 0
down = 0
location = 0
telephone = 0
ai = NPLUS_AI()         
tim1 = Timer(1)
#获取一次app上的电话与住址（app上标注重启拐杖即生效）
phone = conn.recv(1024)#获取qpp的电话
receive = conn.recv(1024)#获取app的地址
dizhi = list(receive)
mp3.volume = 30
uart1 = machine.UART(1, baudrate=115200, tx=Pin.P1, rx=Pin.P6)
uart2 = machine.UART(2, baudrate=115200, tx=Pin.P, rx=Pin.P6)
while True:
    '''data = s.recv(1024)                                 # 从服务器端套接字中读取1024字节数据
    if(len(data) == 0):                                 # 如果接收数据为0字节时,关闭套接字
        print("close socket")
        s.close()
        break
    data=data.decode('utf-8')                         # 以utf-8编码解码字符串'''
    if uart1.read():                                   #存取地址
        location = list(uart1.readline())
    if uart2.read():
        telephone = uart2.readline()
    common()

    #光感手电
    if light.read() < 50:
        p13.write_digital(1)
    else:
        p13.write_digital(0)

    #跌倒报警(ok)
    if get_tilt_angle('X') <= 15 or get_tilt_angle('X') >= 165 or get_tilt_angle('Y') <= 110 or get_tilt_angle('Y') >= 250 or get_tilt_angle('Z') <= -170 or get_tilt_angle('Z') >= -20:
        down = 1
    else:
        down = 0
    
    if down = 1:
        ai.video_capture(60)                 #ai开启摄像头
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
    elif down = 0:
        fall = 0
        timestart = 0
    
    if fall == 1:
        help()
        light()
        sound()
        s.send('call')        #发送消息&定位到app并发警报声
    elif fall == 2:
        help()
        light()
        sound()
        uart2.write(('ATD' + str(phone)))#拨打电话（SIM卡）
    elif fall == 0:
        common()
        music.stop()
            
    #“我想回家，请帮帮我！”
    if p16.read_digital() == 1:              #防止老人按很多次
        backhome = backhome + 1
    if p2.read_digital() == 1:               #方便老人
        backhome = 0
    
    if backhome != 0:                         #按一下“回家”按钮，语音叫路人带他回家并显示家的地址
        home()
        rgb.fill((int(255), int(0), int(0)))
        rgb.write()
        time.sleep_ms(1)
        mp3.singleLoop(1)
        mp3.play_song(1)
        if True：                           #AI摄像头识别到人距离小于46cm时间超过5s
            mp3.stop()
    elif backhome == 0:                       #按下“已回家”按钮，停止
        mp3.singleLoop(0)
        mp3.stop()#停止说话
        common()
    