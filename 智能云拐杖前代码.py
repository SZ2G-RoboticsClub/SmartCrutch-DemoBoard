from mpython import *
import math
import music
import neopixel

my_rgb1 = neopixel.NeoPixel(Pin(Pin.P15), n=21, bpp=3, timing=1)

my_rgb2 = neopixel.NeoPixel(Pin(Pin.P14), n=21, bpp=3, timing=1)

p13 = MPythonPin(13, PinMode.OUT)

global i, j, k, m, n

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

'''
def diedao():
    
    if get_tilt_angle('Y') > 250 and get_tilt_angle('Y') < 300 or get_tilt_angle('Y') > 50 and get_tilt_angle('Y') < 110:
        if get_tilt_angle('X') > -50 and get_tilt_angle('X') < 20 or get_tilt_angle('X') > 170 and get_tilt_angle('X') < 230:
            
            bangwo()
            baosan()
            shengyin()
            
        else:
            music.stop()
            zirandeng()
'''


def baosan():
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


'''
def jibuqi():
    m = 0
    if accelerometer.get_y() > 0 and accelerometer.get_x() > 0:
        m += 1
        oled.DispChar('今天您走了：', 25, 10)
        oled.DispChar('步', 85, 30)
        oled.DispChar((str(m)), 20, 30)
        oled.show()
        sleep_ms(1000)
        oled.fill(0)
'''

def bangwo():
        oled.fill(0)
        oled.DispChar('我摔跤了,请帮帮我！', 15, 20)
        oled.DispChar('联系电话：110 120', 15, 40)
        oled.show()

def shengyin():
    for freq in range(700, 1760, 50):
        music.pitch(freq, 120)
    for freq in range(1760, 700, (-50)):
        music.pitch(freq, 120)

'''
def liushuideng1():
    for i in range(0,255,50):
        for j in range(0,255,50):
            for k in range(0,255,50):
                my_rgb1.fill( (i, j, k) )
                my_rgb2.fill( (i, j, k) )
                my_rgb1.write()
                my_rgb2.write()
        break
'''

    
def zirandeng():
    oled.fill(0)
    oled.DispChar('深圳市第二高级中学', 15, 20)
    oled.DispChar('创客教育研究中心', 15, 40)
    oled.show()
    if light.read() < 50:
        p13.write_digital(1)
    else:
        p13.write_digital(0)
    liushuideng2()

while True:
    
    if get_tilt_angle('Y') > 250 and get_tilt_angle('Y') < 300 or get_tilt_angle('Y') > 50 and get_tilt_angle('Y') < 110:
        if get_tilt_angle('X') > -50 and get_tilt_angle('X') < 20 or get_tilt_angle('X') > 170 and get_tilt_angle('X') < 230:
            
            bangwo()
            baosan()
            shengyin()
            
        else:
            music.stop()
            zirandeng()