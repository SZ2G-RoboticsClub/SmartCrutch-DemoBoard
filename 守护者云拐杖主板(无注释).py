from machine import UART
from mpython import *
import math
import network
import music
import neopixel
import time
import urequests
import audio


# p1 = MPythonPin(1, PinMode.IN)
p0 = MPythonPin(0, PinMode.ANALOG)
my_rgb1 = neopixel.NeoPixel(Pin(Pin.P13), n=63, bpp=3, timing=1)
my_rgb2 = neopixel.NeoPixel(Pin(Pin.P15), n=63, bpp=3, timing=1)


uuid = 'abfb6a0d'
status = 'ok'
heartbeat_Loc = None



BASE_URL = 'http://192.168.43.199:8000/demoboard'


my_wifi = wifi()
my_wifi.connectWiFi("idk","12345678")


GEO_URL = 'http://restapi.amap.com/v3/geocode/geo?address='
R_GEO_URL= 'http://restapi.amap.com/v3/geocode/regeo?output='
NAV_URL = 'http://restapi.amap.com/v3/direction/walking?'
key = '10d4ac81004a9581c1d9de89eac4035b'


api_key = 'Lcr1un815AuFGa7DZDQv1sqx'
secret_key = 'ujfZqO3mgcQZ52nXsfC9je02IiRDjaFb'
method = ''
nav_file = 'nav_file.mp3'


lat_home = 0
lon_home = 0
home_loc = ''

backhome = 0
ori_loc = ''
para_nav = ''

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

switch = 0                                     
move = 0
down = 0
fall = 0
time_on = None
time_set = None
dial = 0



oled.fill(0)
oled.DispChar('初始化完毕', 0, 0)
oled.show()


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
    # global freq
    oled.fill(0)
    oled.DispChar('我摔跤了,请帮帮我！', 15, 20)
    oled.show()
    # for freq in range(880, 1930, 35):
    #     music.pitch(freq, 50)
    # for freq in range(1930, 880, -35):
    #     music.pitch(freq, 50)

    # TEST4
    # for p in range(2):
    #   audio.play('alarm.mp3')
    #   time.sleep(1)

    # TEST5
    music.play(music.JUMP_UP, wait=True, loop=False)


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


def rainbow():
    global move
    make_rainbow(my_rgb1, 63, 80, move)
    make_rainbow(my_rgb2, 63, 80, move)
    my_rgb1.write()
    my_rgb2.write()
    # time.sleep(0.25)  
    move = move - 1


def on_button_a_pressed(_):
    global switch
    switch += 1

button_a.event_pressed = on_button_a_pressed


def common():
    global switch
    oled.fill(0)
    oled.DispChar('守护者云拐杖', 24, 16)
    oled.DispChar('开', 56, 32)
    oled.show()
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


def message():
    pass


def sec_message():
    pass



def fall_det():
    global loc_cycle, loc_info, dial, loc_get1, location1, a1, a2, b1, b2, c1, c2, x, time_on, down, fall, lat_now, lon_now, status, heartbeat_Loc

    x = accelerometer.get_x()

    if x <= 0.5:
        down = 1
    else:
        down = 0


    if down == 1:
        if time_on == None:
            time_on = time.time()
        
        my_rgb1.fill( (255, 0, 0) )
        my_rgb2.fill( (255, 0, 0) )
        my_rgb1.write()
        my_rgb2.write()

        if time.time() - time_on > 10 and time.time() - time_on <= 30:
            fall = 1
        if time.time() - time_on > 30:
            fall = 2

    elif down == 0:
        fall = 0
        time_on = None


    if fall == 1:
        status = 'emergency'
        flashlight()
        help()
        message()


    if fall == 2:
        status = 'emergency'
        flashlight()
        help()
        sec_message()
        if dial == 0:

            # TEST1
            # oled.fill(0)
            # oled.DispChar('已拨打电话', 0, 0)
            # oled.show()
            # print('已拨打电话')
            # time.sleep(1)
            # oled.fill(0)
            # oled.show()

            uart2.write('AT+SETVOLTE=1')
            time.sleep(3)
            uart2.write('ATD' + str(user_set.get('settings').get('phone')))
            
            dial = 1

    if fall == 0:

        if dial == 1:
            uart2.write('AT+CHUP')
            dial = 0

        music.stop()
        common()
        status = 'ok'


def on_button_b_pressed(_):
    global backhome
    backhome = 1

button_b.event_pressed = on_button_b_pressed


def take_u_home():
    global backhome, loc_cycle, method, _f, para_nav, nav, NAV_URL, lat_now, lon_now, ori_loc, data_audio, nav_file, r_audio 
    
    if backhome == 1:
        ori_loc = loc_cycle
        # oled.fill(0)
        # oled.DispChar('当前位置记录完毕', 0, 16)
        # oled.DispChar(ori_loc, 0, 32)
        # oled.show()
        # time.sleep(3)
        # oled.fill(0)
        # oled.show()
        # print(ori_loc)
        para_nav = 'origin='+ori_loc+'&destination='+home_loc+'&key='+key
        # print(para_nav)
        nav = urequests.get(url=NAV_URL+str(para_nav))
        # print(nav)
        nav = nav.json()
        # print(nav)
        if nav.get('status') == "1":
            # oled.fill(0)
            # oled.DispChar('守护者云拐杖', 24, 16)
            # oled.DispChar('正在带您回家', 24, 40)
            # oled.show()
            method = nav.get('route').get('paths')[0].get('steps')[0].get('instruction')
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
            audio.stop()

        elif nav.get('status') != "1":
            # oled.fill(0)
            # oled.DispChar('守护者云拐杖', 24, 16)
            # oled.DispChar('导航结束', 40, 32)
            # oled.show()
            audio.play('nav_end.mp3')
            time.sleep(3)
            audio.stop()
            
            backhome = 0
                # break
            


def heartbeat():
    global uuid, status, heartbeat_Loc, data, resp
    data = {
    "uuid": uuid,
    "status":status,
    "loc": heartbeat_Loc
    }

    resp = urequests.post(url=BASE_URL+'/heartbeat', json=data)

    resp = resp.json()



# ai = NPLUS_AI()
# ai.mode_change(1)
audio.player_init(i2c)
audio.set_volume(100)
uart1 = machine.UART(1, baudrate=9600, tx=Pin.P11, rx=Pin.P14)
uart2 = machine.UART(2, baudrate=9600, tx=Pin.P15, rx=Pin.P16)


s = urequests.get(url=BASE_URL+'/get_settings/'+uuid)
user_set = s.json()
if user_set.get('code') == 0:
    oled.DispChar('获取账户连接成功', 0, 0)
    oled.show()
    time.sleep(1)
    oled.fill(0)
    oled.show()
    
    home = user_set.get('settings').get('home')
    h = urequests.get(url=GEO_URL+home+'&output=json&key='+key)
    h = h.json()

    home_loc = h.get('geocodes')[0].get('location')
    oled.DispChar('家庭位置记录完毕', 0, 16)
    oled.DispChar(home_loc, 0, 32)
    oled.show()
    time.sleep(1)
    oled.fill(0)
    oled.show()

    while True:
        
        while True:
            loc_get1 = uart1.readline()
            if loc_get1:
                break

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

        # TEST2
        # lon_now = 113.937507
        # lat_now = 22.570334

        loc_cycle = str(lon_now) + ',' + str(lat_now)

        heartbeat_Loc = {
            "latitude": lat_now,
            "longitude": lon_now
            }

        if time_set == None:
            time_set = time.time()

        take_u_home()

        if time.time() - time_set >= 5:
            heartbeat()
            time_set = None
            if resp.get('code') == 0:
                continue
            elif resp.get('code') == 1:
                print('拐杖未注册')
            else:
                oled.fill(0)
                oled.DispChar('心跳包错误', 0, 0, 1)
                oled.show()

                # TEST3
                print(resp.get('msg'))

                # time.sleep(1)
                # oled.fill(0)
                # oled.DispChar(str(resp.get('msg')), 0, 0, 1, True)
                # oled.show()
else:
    # print('账户连接失败，请重新启动')
    oled.fill(0)
    oled.DispChar('账户连接失败，请重新启动', 0, 0, 1, True)
    oled.show()