from machine import UART
from mpython import *
from ai import *
import math
import network
import music
import neopixel
import time
import urequests
import ubinascii
import audio
import gc


uart1 = machine.UART(1, baudrate=9600, tx=Pin.P13, rx=Pin.P14)



# 主控板引脚：
# p16tx&p9rx：串口uart2(SIM卡模块)
# p13tx&p14rx：串口uart1(北斗定位模块)
# p0&p1：前（choice=1）后（choice=2）摄像头控制
# B键(P11)(绿色按钮): "带我回家"按钮+中断导航
# p2(红色按钮)：照明灯开关
# p3：光敏电阻（光线传感）
# p8：掌控板喇叭
# p7：灯带1（灯数：63/24）
# p15：灯带2（灯数：63/24）

# PCB接线特殊处：
# 上下两板0,1连通但要0对1、1对0
# 上板SIM卡模块的TXD与p0相连，RXD与p1相连————SIM卡与摄像头模块共用串口uart2
# 上板PWR与GND均要与下板相连
# 上板中摄像头的VCC正极无需接线，但必须接GND
# 上下两板的p8要连通，上板P8旁GND非必须连接
# 上板一定要有天线
# 上板调试串口直连USB时，PWR需连接5V接口


# 摔倒判断：
# x轴加速度是否小于0.5（平行于屏幕方向向下为正方向）


# 位置获取：
# 使用高德地图api 
# a: list
# b, c: float
# a1b1c1为纬度数据，a2b2c2为经度数据


# 实时定位位置：
# loc_get1, location1, a/b/c:1&2

# 开机流程
# 灯带1亮白灯1s：程序启动成功
# 灯带2亮白灯1s: wifi连接成功
# 灯带1与2均亮白灯1s：网络初始化完毕

# 灯带1亮绿灯1s：摄像头初始化成功
# 灯带2亮绿灯1s：urequests成功
# 灯带1与2均亮绿灯1s：摄像头与SIM测试完成

# 灯带1与2均亮绿灯闪烁一次（亮灭亮）：开始进入主循环


p2 = MPythonPin(2, PinMode.IN)
p11 = MPythonPin(11, PinMode.IN)
p3 = MPythonPin(3, PinMode.ANALOG)

my_rgb1 = neopixel.NeoPixel(Pin(Pin.P7), n=63, bpp=3, timing=1)
my_rgb2 = neopixel.NeoPixel(Pin(Pin.P15), n=63, bpp=3, timing=1)

# my_rgb1 = neopixel.NeoPixel(Pin(Pin.P7), n=24, bpp=3, timing=1)
# my_rgb2 = neopixel.NeoPixel(Pin(Pin.P15), n=24, bpp=3, timing=1)

uart1.write('switch on\r\n')
my_rgb1.fill((255, 255, 255))
my_rgb1.write()
time.sleep(1)
my_rgb1.fill((0,0,0))
my_rgb1.write()
uart1.write('switch success\r\n')

#心跳包数据初始化
uuid = 'fbb72bd8'        #拐杖身份证
status = 'ok'                      #拐杖状态（"ok"/"emergency"/"error"/"offline"）
heartbeat_Loc = None             #location



#初始化服务器传输

# 本地
# BASE_URL = 'http://192.168.1.104:8000/demoboard'     #QFCS1
# BASE_URL = 'http://192.168.1.107:8000/demoboard'     #QFCS2
# BASE_URL = 'http://192.168.31.132:8000/demoboard'    #QFCS-MI
# BASE_URL = 'http://192.168.43.199:8000/demoboard'    #idk
# BASE_URL = 'http://192.168.0.110:8000/demoboard'     #Tenda_7C8540
# BASE_URL = 'http://192.168.3.239:8000/demoboard'     #NPlus
BASE_URL = 'http://192.168.103.87:8000/demoboard'    #啊哈

# 公网服务器
# BASE_URL = 'http://39.103.138.199:8000/demoboard'



#搭建WiFi，连接app用户手机数据
uart1.write('connectWiFi\r\n')

my_wifi = wifi()
my_wifi.connectWiFi("啊哈","dy666821")


my_rgb2.fill((255, 255, 255))
my_rgb2.write()
time.sleep(1)
my_rgb2.fill((0,0,0))
my_rgb2.write()
uart1.write('connected\r\n')


#路径规划初始化
GEO_URL = 'http://restapi.amap.com/v3/geocode/geo?address='   #高德地图
NAV_URL = 'http://restapi.amap.com/v3/direction/walking?'
R_GEO_URL= 'http://restapi.amap.com/v3/geocode/regeo?output=json&location='

key_dy = '10d4ac81004a9581c1d9de89eac4035b'
key_zhs = '9e13f3028c7714a7a15af2e7e45a915c'
key_hg = '09f9a9b0494e3d0eb8b75b16435e4d9f'



#百度语音导航初始化
api_key = 'Lcr1un815AuFGa7DZDQv1sqx'        
secret_key = 'ujfZqO3mgcQZ52nXsfC9je02IiRDjaFb'
method = ''
nav_file = 'nav_file.mp3'



#家庭住址经纬信息
lat_home = 0
lon_home = 0
home_loc = ''

backhome = 0
ori_loc = ''
para_nav = ''

st = 0



#实时获取老人定位
lat_now = 0
lon_now = 0
loc_info = ''
tran = ''
loc_cycle = ''
location1 = []
m = ''
a1 = []
a2 = []
b1 = 0
b2 = 0
c1 = 0
c2 = 0



#全局变量定义       
p = 0
switch = 0                    
stop = 0        #中断导航变量
move = 0        #彩虹灯变量
down = 0        #0：拐杖没倒；    1：拐杖倒了
fall = 0        #0：没摔倒；   1：摔倒了且已过了10s；    2：摔倒了30s
time_on = None     #摔倒初始时间
time_set = None    #心跳包发送初始时间
geo_time = None
video_time = None
dial = 0         #拨号：      1：已拨号一次         0：未拨过号
choice = 0


# print('网络连接初始化完毕')

uart1.write('network and variables definition\r\n')
my_rgb1.fill((255,255,255))
my_rgb1.write()
my_rgb2.fill((255,255,255))
my_rgb2.write()
time.sleep(1)
my_rgb1.fill((0,0,0))
my_rgb1.write()
my_rgb2.fill((0,0,0))
my_rgb2.write()
uart1.write('network and variables definition ok\r\n')

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
    
    # make_rainbow(my_rgb1, 24, 80, move)
    # make_rainbow(my_rgb2, 24, 80, move)
    my_rgb1.write()
    my_rgb2.write()
    # time.sleep(0.25)  
    move = move - 1



#平常状态(ok)
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
        if p3.read_analog() < 100:
            my_rgb1.fill( (255, 255, 255) )
            my_rgb2.fill( (255, 255, 255) )
            my_rgb1.write()
            my_rgb2.write()
            time.sleep_ms(500)
        elif p3.read_analog() >= 100:
            rainbow()    
    elif switch % 3 == 2:
        my_rgb1.fill( (255, 255, 255) )
        my_rgb2.fill( (255, 255, 255) )
        my_rgb1.write()
        my_rgb2.write()



# 实时位置获取
def getLoc_now():
    global r_geo, geo_time, loc_get1, location1, a1, b1, c1, a2, b2, c2, lat_now, lon_now, loc_cycle, loc_info, tran
    if geo_time == None:
        geo_time = time.time()
        
    if time.time() - geo_time >= 4:
        # while True:
        #     loc_get1 = uart1.readline()
        #     if loc_get1:
        #         break
        # location1 = (str(loc_get1).split(','))

        m = '$GNGLL,2234.41586,N,11356.00044,E,051136.000,A,A*4E'
        location1 = m.split(',')

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
        
        # TEST9
        # lon_now = 114.095582
        # lat_now = 22.565531

        loc_cycle = str(lon_now) + ',' + str(lat_now)
        
        # debug11
        # print(R_GEO_URL+loc_cycle+'&key='+key_zhs)
                
        # r_geo = urequests.get(url=R_GEO_URL+loc_cycle+'&key='+key_zhs)
        # r_geo = r_geo.json()

        # debug9
        # print(r_geo)
        
        # country_ = r_geo.get('regeocode').get('addressComponent').get('country')
        # province_ = r_geo.get('regeocode').get('addressComponent').get('province')
        # city_ = r_geo.get('regeocode').get('addressComponent').get('city')
        # loc_info = r_geo.get('regeocode').get('formatted_address')
        # loc_info = loc_info.replace(country_, '').replace(province_, '').replace(city_, '')
        
        # debug10
        # print(loc_info)
        
        # TEST8
        loc_info = '深圳市第二高级中学'
    
        tran = ubinascii.hexlify(loc_info.encode('utf-8'))
        tran = tran.decode()
        geo_time = None
        
        # debug12
        # print(tran)
        # print(type(tran))



# 摄像头切换摄像
def recordVideo():
    global video_time, choice, p

    if video_time == None:
        # p += 1
        video_time = time.time()
        # time.sleep(3)
        # print('ok000')
        # ai.AI_WaitForARP(0x34,[1])
        ai.AI_WaitForARP(0x34,[choice])
        # print('ok', p)
        ai.AI_Uart_CMD(0x3B,[int(4/2),0,0,0])
        # print('okk', p)
        choice = (choice + 1) % 2

    if time.time() - video_time >= 5:              # 缓冲开始摄像时间2s
        video_time = None



# ============ Functions ============

#摔倒检测(ok)
def fall_det():
    global loc_cycle, loc_info, dial, loc_get1, location1, a1, a2, b1, b2, c1, c2, x, time_on, down, fall, lat_now, lon_now, status, heartbeat_Loc

    z = accelerometer.get_z()
    #拐杖倒地判定
    if z <= 0.6:            #究其根本
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
        if time.time() - time_on > 2 and time.time() - time_on <= 5:
            fall = 1
        #30s内没起来
        if time.time() - time_on > 5:
            fall = 2

    elif down == 0:
        fall = 0
        time_on = None


    if fall == 1:
        status = 'emergency'
        lon_now = 113.937507
        lat_now = 22.570334
        flashlight()
        music.play(music.JUMP_UP, pin=Pin.P8, wait=True, loop=False)


    if fall == 2:
        uart1.write('the second alarm!!!\r\n')
        if dial == 0:
            k = uart2.read()
            
            uart2.write('ATH\r\n')
            time.sleep(1)
            
            # 倒地30s后SIM模块拨打setting中紧急联系人电话
            # uart2.write('ATD' + str(user_set.get('settings').get('phone')) + ';\r\n')
            uart2.write('ATD18129922583;\r\n')
            time.sleep(2)

            dial = 1
        status = 'emergency'
        lon_now = 113.937507
        lat_now = 22.570334
        flashlight()
        music.play(music.JUMP_UP, pin=Pin.P8, wait=True, loop=False)
        # print('')
       
    if fall == 0:

        if dial == 1:
            k = uart2.read()
            uart2.write('ATH\r\n') #(挂断所有通话)
            dial = 0

        music.stop()
        common()
        status = 'ok'



#"带你回家"
def take_u_home():
    global stop, st, backhome, loc_cycle, method, _f, para_nav, nav, NAV_URL, lat_now, lon_now, ori_loc, data_audio, nav_file, r_audio 

    if p11.read_digital() == 1:
        backhome += 1
        time.sleep_ms(350)

    if backhome % 2 == 1:
        stop = 1
        
        # debug3
        # print('开始导航')
        uart1.write('navigation\r\n')
        my_rgb1.fill((0,0,255))
        my_rgb1.write()
        time.sleep(1)
        my_rgb1.fill((0,0,0))
        my_rgb1.write()
        
        if st == 0:
            ori_loc = loc_cycle
            st = 1
        elif st == 1:
            ori_loc = '113.937507,22.570334'
            st = 0
        # print('当前位置记录完毕', ori_loc)
        para_nav = 'origin='+ori_loc+'&destination='+home_loc+'&key='+key_dy
        # print(NAV_URL+str(para_nav))
        nav = urequests.get(url=NAV_URL+str(para_nav))
        # print(nav)
        nav = nav.json()
        # print(nav)
        
        uart1.write('navigation prepared\r\n')
        my_rgb2.fill((0,0,255))
        my_rgb2.write()
        time.sleep(1)
        my_rgb2.fill((0,0,0))
        my_rgb2.write()
                
        
        if nav.get('status') == "1":
            # print('守护者云拐杖正在带您回家')
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
            
            uart1.write('navigation spoken out\r\n')
            my_rgb2.fill((0,0,255))
            my_rgb2.write()
            my_rgb1.fill((0,0,255))
            my_rgb1.write()
            time.sleep(1)
            my_rgb2.fill((0,0,0))
            my_rgb2.write()
            my_rgb1.fill((0,0,0))
            my_rgb1.write()
            
            
            # debug4
            # print(method)
            
            time.sleep(5)
            audio.stop()
            

            if nav.get('route').get('paths')[0].get('steps')[0].get('assistant_action') == "到达目的地":
                
                # TEST7
                # print('导航结束')
                uart1.write('navigation end\r\n')
                for o in range(2):
                    time.sleep(0.5)
                    my_rgb1.fill((0,0,255))
                    my_rgb1.write()
                    my_rgb2.fill((0,0,255))
                    my_rgb2.write()
                    time.sleep(0.5)
                    my_rgb2.fill((0,0,0))
                    my_rgb2.write()
                    my_rgb1.fill((0,0,0))
                    my_rgb1.write()

                audio.play('nav_end.mp3')
                time.sleep(1)
                audio.stop()
                
                backhome = 0
                stop = 0
    elif backhome % 2 == 0:
        # print('停了')
        if stop == 1:
            # print('已中断')
            uart1.write('navigation interupted\r\n')
            stop = 0

        fall_det()
            


#心跳包发送(ok)
def heartbeat():
    global uuid, status, heartbeat_Loc, data, resp
    data = {
        "uuid": uuid, 
        "status":status, 
        "loc": heartbeat_Loc
    }
    
    # debug7
    # print(data)
    
    resp = urequests.post(url=BASE_URL+'/heartbeat', json=data)       #发送心跳包
    resp = resp.json()




# ============ Main ============

uart1.write('camera init\r\n')
ai = NPLUS_AI()

my_rgb1.fill((0,255,0))
my_rgb1.write()
time.sleep(1)
my_rgb1.fill((0,0,0))
my_rgb1.write()
uart1.write('camera init ok\r\n')

audio.player_init(i2c)
audio.set_volume(100)
# uart1 = machine.UART(1, baudrate=9600, tx=Pin.P13, rx=Pin.P14)
uart2 = machine.UART(2, baudrate=115200, tx=Pin.P1, rx=Pin.P0)


#获得settingdata拐杖状态
uart1.write('urequests\r\n')
s = urequests.get(url=BASE_URL+'/get_settings/'+uuid)
user_set = s.json()

my_rgb2.fill((0,255,0))
my_rgb2.write()
time.sleep(1)
my_rgb2.fill((0,0,0))
my_rgb2.write()
uart1.write('urequests ok\r\n')

if user_set.get('code') == 0:
    # print('获取账户连接成功')
    q = 0
    
    # 开机测试
    uart1.write('camera tests\r\n')
    ai.AI_WaitForARP(0x34,[1])
    ai.AI_Uart_CMD(0x3B,[int(2/2),0,0,0])
    # print('camera ok')
    uart1.write('camera0 done\r\n')
    
    time.sleep(1)
    ai.AI_WaitForARP(0x34,[1])
    ai.AI_Uart_CMD(0x3B,[int(2/2),0,0,0])
    # print('camera actually ok')   
    uart1.write('camera1 done\r\n')
    time.sleep(1)
    
    uart1.write('SIM tests\r\n')                                                                            
    
    k = uart2.read()
    uart2.write('ATH\r\n')
    time.sleep(1)
    # print('ready to go on')
    
    # uart2.write('ATD13724285352;\r\n')
    k = uart2.read()
    uart2.write('ATD18129922583;\r\n')
    # uart2.write('ATD15302678343;\r\n')
    time.sleep(5)
    uart1.write(str(uart2.read())+'\r\n')
    # print('has called it up')
    
    # time.sleep(15)
    # uart2.write('ATD18129922583;\r\n')
    # uart1.write('another')
    
    while True:
        if p11.read_digital() == 1:
            q += 1
            
            k = uart2.read()
            uart2.write('ATH\r\n')
            uart1.write('hang up\r\n')
            time.sleep(1)
            
            k = uart2.read()
            # uart2.write('ATD13724285352;\r\n')
            uart2.write('ATD18129922583;\r\n')
            # uart2.write('ATD15302678343;\r\n')
            uart1.write('retry'+str(q)+'\r\n')
            time.sleep(2)
            uart1.write(str(uart2.read()))
        # print('has called it up')
            
        if uart2.any():
            uart1.write(uart2.read() + '\r\n')
            # print(uart2.read())
            # print(bytes.decode(uart2.read()))
        if p2.read_digital() == 1:
            uart2.write('ATH\r\n')
            uart1.write('SIM done\r\n')
            break
    
    uart1.write('final success\r\n')
    my_rgb1.fill((0,255,0))
    my_rgb1.write()
    my_rgb2.fill((0,255,0))
    my_rgb2.write()
    time.sleep(1)
    my_rgb2.fill((0,0,0))
    my_rgb2.write()
    my_rgb1.fill((0,0,0))
    my_rgb1.write()
    
    
    # 家庭住址经纬度获取
    home = user_set.get('settings').get('home')

    # debug1
    # print(user_set)
    # print("home", home)

    h = urequests.get(url=GEO_URL+home+'&output=json&key='+key_dy)
    h = h.json()

    # debug2
    # print(h)

    home_loc = h.get('geocodes')[0].get('location')
    
    # debug5
    # print(home_loc)
    
    # print('家庭位置记录完毕', home_loc)
    
    time.sleep(2)
    uart1.write('main loop start')
    for o in range(2):
        time.sleep(0.5)
        my_rgb1.fill((0,255,0))
        my_rgb1.write()
        my_rgb2.fill((0,255,0))
        my_rgb2.write()
        time.sleep(0.5)
        my_rgb2.fill((0,0,0))
        my_rgb2.write()
        my_rgb1.fill((0,0,0))
        my_rgb1.write()


    while True:
        gc.collect()
        
        getLoc_now()
        recordVideo()     
        
        take_u_home()
        # fall_det()
        
        heartbeat_Loc = {
            "longitude": lon_now, 
            "info": tran, 
            "latitude": lat_now
            }
            
        # heartbeat_Loc = None
    
        if time_set == None:
            time_set = time.time()
    
        if time.time() - time_set >= 5:
            
            # debug6
            # print(loc_cycle)
            # print(heartbeat_Loc)
            
            heartbeat()
            time_set = None
            if resp.get('code') == 0:                   #返回数据类型正常
                continue
            elif resp.get('code') == 1:
                print('拐杖未注册')
            else:
                print('心跳包错误')
                print(resp)


else:
    print('账户连接失败，请重新启动')



#状态：倒地，common()，导航