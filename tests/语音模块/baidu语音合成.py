from mpython import *
import audio
import network
import neopixel
import urequests
import time
import gc

my_rgb1 = neopixel.NeoPixel(Pin(Pin.P7), n=63, bpp=3, timing=1)
my_rgb2 = neopixel.NeoPixel(Pin(Pin.P15), n=63, bpp=3, timing=1)

my_wifi = wifi()
# my_wifi.connectWiFi('QFCS-MI', '999999999')
my_wifi.connectWiFi('啊哈', 'dy666821')

my_rgb1.fill((0,255,0))
my_rgb1.write()
time.sleep(1)
my_rgb1.fill((0,0,0))
my_rgb1.write()

p11 = MPythonPin(11, PinMode.IN)
p2 = MPythonPin(2, PinMode.IN)


audio.player_init(i2c)
audio.set_volume(100)
file = 'nav_file.mp3'

switch = 0
move = 0
backhome = 0
st = 0

def make_rainbow(_neopixel, _num, _bright, _offset):          
    _rgb = ((255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,255,255), (0,0,255), (136,0,255), (255,0,0))
    for i in range(_num):
        t = 7 * i / _num
        t0 = int(t)
        r = round((_rgb[t0][0] + (t-t0)*(_rgb[t0+1][0]-_rgb[t0][0]))*_bright)>>8
        g = round((_rgb[t0][1] + (t-t0)*(_rgb[t0+1][1]-_rgb[t0][1]))*_bright)>>8
        b = round((_rgb[t0][2] + (t-t0)*(_rgb[t0+1][2]-_rgb[t0][2]))*_bright)>>8
        _neopixel[(i + _offset) % _num] = (r, g, b)
        

def rainbow():
    global move
    make_rainbow(my_rgb1, 63, 80, move)
    make_rainbow(my_rgb2, 63, 80, move)
    
    # make_rainbow(my_rgb1, 24, 80, move)
    # make_rainbow(my_rgb2, 24, 80, move)
    my_rgb1.write()
    my_rgb2.write()
    # time.sleep(0.25)  
    move = move - 1
    
    
def common():
    global switch
    if p2.read_digital() == 1:      # 开关灯
        switch += 1
        time.sleep_ms(350)
        
    #光感手电
    if switch % 3 == 0:
        my_rgb2.fill((0,0,0))
        my_rgb1.fill((0,0,0))
        my_rgb1.write()
        my_rgb2.write()
    elif switch % 3 == 1:
        rainbow()
    elif switch % 3 == 2:
        my_rgb1.fill( (255, 255, 255) )
        my_rgb2.fill( (255, 255, 255) )
        my_rgb1.write()
        my_rgb2.write()


my_rgb2.fill((0,255,0))
my_rgb2.write()
time.sleep(1)
my_rgb2.fill((0,0,0))
my_rgb2.write()
while True:
    gc.collect()
    common()
    if p11.read_digital() == 1:
        backhome += 1
        
        my_rgb1.fill((0,0,255))
        my_rgb1.write()
        time.sleep(1)
        my_rgb1.fill((0,0,0))
        my_rgb1.write()
        
    if backhome >= 1:
        if st % 3 == 0:
            method = '向西步行1米左转'
        elif st % 3 == 1:
            method = '向南步行37米右转'
        elif st % 3 == 2:
            method = '向西步行3米，到达目的地'
            
        my_rgb2.fill((0,0,255))
        my_rgb2.write()
        time.sleep(1)
        my_rgb2.fill((0,0,0))
        my_rgb2.write()
        
        baidu_params = {
            "API_Key": 'Lcr1un815AuFGa7DZDQv1sqx', 
            "Secret_Key": 'ujfZqO3mgcQZ52nXsfC9je02IiRDjaFb', 
            "text": method, 
            "filename": file
        }
        
        _rsp = urequests.post("http://119.23.66.134:8085/baidu_tts", params=baidu_params)
        with open(file, "w") as _f:
            while True:
                dat = _rsp.recv(1024)
                if not dat:
                    break
                _f.write(dat)
        
        my_rgb2.fill((0,0,255))
        my_rgb2.write()
        my_rgb1.fill((0,0,255))
        my_rgb1.write()
        time.sleep(1)
        my_rgb2.fill((0,0,0))
        my_rgb2.write()
        my_rgb1.fill((0,0,0))
        my_rgb1.write()
        audio.play(file)
        time.sleep(5)
        
        st += 1
        if st % 3 == 2:
            break



my_rgb2.fill((0,0,255))
my_rgb2.write()
my_rgb1.fill((0,0,255))
my_rgb1.write()
time.sleep(1)
my_rgb2.fill((0,0,0))
my_rgb2.write()
my_rgb1.fill((0,0,0))
my_rgb1.write()
audio.play('nav_end.mp3')
# print('ok')
# while True:
#     gc.collect()
#     if p2.read_digital() == 1:
#         print('现在开始')
#         time.sleep(1)
#         audio.play(file)
#         time.sleep(1)

