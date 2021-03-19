from machine import Timer
from mpython import *
from bluebit import *
import smartcamera
import math
import music
import neopixel
import radio
import time
import requests

#p1：心率传感器（模拟值需测试）
#p13：rgb灯
#p14 灯带1
#p15：灯带2
#p16：“回家”按钮
#p0：MP3模块

#song1 = “我想回家，请帮帮我！”
#

my_rgb1 = neopixel.NeoPixel(Pin(Pin.P15), n=21, bpp=3, timing=1)#变量与引脚设定
my_rgb2 = neopixel.NeoPixel(Pin(Pin.P14), n=21, bpp=3, timing=1)
mp3 = MP3(Pin.P0)
a = 0
move = 0

p13 = MPythonPin(13, PinMode.OUT)
p1 = MPythonPin(1, PinMode.ANALOG)

radio.on()                 #无线电广播功能打开
radio.config(channel=13)

#global i, j, k, m, n,

def get_tilt_angle(_axis):                                    #加速度计设定(ok)
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

def help():                                                   #呼叫路人来帮忙(ok)
    oled.fill(0)
    oled.DispChar('我摔跤了,请帮帮我！', 15, 20)
    oled.show()
    sound()
    pass
    
def sound():                                                  #MP3发警报声(ok)
    music.play(music.POWER_UP, wait=False, loop=True)

def common():                                                 #平常状态
    oled.fill(0)
    oled.DispChar('智能云拐杖', 24, 16)
    oled.DispChar('开', 56, 32)
    oled.show()
    liushuideng()
       
def timer1_tick(_):                                           #发送心跳pulse到服务端
    global pulse
    pulse = ((1024 - 0) / (4095 - 0)) * (p1.read_analog() - 0) + 0    #要测试心率映射值
    radio.send(str(pulse))

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

def home():                                                   #“回家”住址自动换行显示
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

smartcamera = smartcamera.SmartCamera(tx=Pin.P2, rx=Pin.P7)         #AI摄像头开启
smart_camera.sensor.reset()
smart_camera.sensor.set_framesize(smart_camera.sensor.VGA)
smart_camera.sensor.set_pixformat(smart_camera.sensor.RGB565)
smart_camera.sensor.set_auto_whitebal(True)
smart_camera.sensor.run(1)
tim1 = Timer(1)
#获取一次app上的电话与住址（app上标注重启拐杖即生效）
receive = #获取app的地址
phone = #获取qpp的电话
dizhi = list(receive)
mp3.volume = 30
while True:
    common()
    #手电
    if light.read() < 50:
        p13.write_digital(1)
    else:
        p13.write_digital(0)
    #心率每小时定时发送
    tim1.init(period=3600000, mode=Timer.PERIODIC, callback=timer1_tick)
    #跌倒报警
    if get_tilt_angle('Y') > 250 and get_tilt_angle('Y') < 300 or get_tilt_angle('Y') > 50 and get_tilt_angle('Y') < 110:
        if get_tilt_angle('X') > -50 and get_tilt_angle('X') < 20 or get_tilt_angle('X') > 170 and get_tilt_angle('X') < 230:
        #计时10s，如果10s内重力方向没起来或起来了但无正常加速度，则：
            help()
            light()
            sound()
            #或：music.play(music.POWER_UP, wait=False, loop=True)
            #发送消息&定位到app

            #30s还没起来，拨电话（SIM）卡
         
        else:           #起来了，则停止
            music.stop()
            common()
    #按“回家”按钮，语音叫路人带他回家并报给路人家的地址
    if p16.read_digital() == 1:
        a = a + 1
    #AI摄像头说：“我想回家，请帮帮我！”
    if a % 2 == 1:
        home()
        mp3.singleLoop(1)
        mp3.play_song(1)
    elif a % 2 == 0:
        mp3.singleLoop(0)
        mp3.stop()#停止说话
        common()
    #拐杖记录仪（AI摄像头）
