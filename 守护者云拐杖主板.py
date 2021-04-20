from machine import UART
from mpython import *
from bluebit import *
from nplus.ai import *
import math
import network
import music
import neopixel
import time
import urequests




#引脚：
#p16tx&p15rx：串口uart2(SIM卡模块)
#p14tx&p11rx：串口uart1(北斗定位模块)——测试用的是北斗，北斗只输入14tx引脚不输出
#p0&p1：小方舟模块
#p13：灯带
#掌控板a键：“带我回家”按钮

#摔倒判断：角度

#小方舟学习数据：id0为充电座上的二维码




my_rgb = neopixel.NeoPixel(Pin(Pin.P13), n=24, bpp=3, timing=1)

#心跳包数据初始化
uuid = '3141592653589793'        #拐杖身份证
status = ""                      #拐杖状态（"ok"/"emergency"/"error"/"offline"）
heartbeat_Loc = None             #location

#初始化服务器传输
BASE_URL = 'http://192.168.31.125:8000/demoboard'
my_wifi = wifi()         #搭建WiFi，连接app用户手机数据
my_wifi.connectWiFi("QFCS-MI","999999999")

#路径规划初始化
MAP_URL = ''
ak = 'CZHBGZ6TXADxI2UecA1xfpq2GtKLMYam'

#全局变量定义                                            
backhome = 0    #1：按下带我回家按钮；   0：导航到家或空状态
move = 0        #彩虹灯变量
down = 0        #0：拐杖没倒；    1：拐杖倒了
fall = 0        #0：没摔倒；   1：摔倒了且已过了10s；    2：摔倒了30s
time_on = 0     #摔倒初始时间
switch = 0      #0：充电状态；     1：不在充电
location1 = []    #充电结束获取的经纬信息
loc_get1 = []
location2 = []    #摔倒获取的经纬信息
loc_get2 = []
location3 = []    #按下回家按钮获取的经纬信息
log_get3 = []
lat_first = 0
lon_first = 0
lat_now = 0
lon_now = 0
lat_fall = 0
lon_fall = 0
# ori_loc = 0
# des_loc = 0
# parameters = 0
home_lock = 0     #（home_thread调用）0:空状态    1：记录完一次经纬度
c_lock = 0
#（crutchlock，fall_det_thread调用）
# -1：充电状态；   
# 1：正在使用；   
# 0：充电结束记录完初始经纬度；   
# 2：摔倒记录完倒地经纬度



# ============ Module ============

#加速度计
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


#平常状态之彩虹灯效设定
def make_rainbow(_neopixel, _num, _bright, _offset):          
    _rgb = ((255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,255,255), (0,0,255), (136,0,255), (255,0,0))
    for i in range(_num):
        t = 7 * i / _num
        t0 = int(t)
        r = round((_rgb[t0][0] + (t-t0)*(_rgb[t0+1][0]-_rgb[t0][0]))*_bright)>>8
        g = round((_rgb[t0][1] + (t-t0)*(_rgb[t0+1][1]-_rgb[t0][1]))*_bright)>>8
        b = round((_rgb[t0][2] + (t-t0)*(_rgb[t0+1][2]-_rgb[t0][2]))*_bright)>>8
        _neopixel[(i + _offset) % _num] = (r, g, b)


#呼叫路人来帮忙
def help():
    oled.fill(0)
    oled.DispChar('我摔跤了,请帮帮我！', 15, 20)
    oled.show()
    music.play(music.POWER_UP, wait=True, loop=False)


#倒地闪红蓝报警灯
def flashlight():                                                  
    for i in range(2):
        my_rgb.fill( (255, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (255, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 255) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 255) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (255, 255, 255) )
        my_rgb.write()
        time.sleep_ms(50)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep_ms(50)


#平常状态之流水彩虹灯
def rainbow():
    make_rainbow(my_rgb, 23, 80, move)
    my_rgb.write()
    time.sleep(0.25)
    move = move + 1


#平常状态(ok)
def common():
    oled.fill(0)
    oled.DispChar('智能云拐杖', 24, 16)
    oled.DispChar('开', 56, 32)
    oled.show()
    rainbow()
    #光感手电
    if light.read() < 50:
        my_rgb.fill( (255, 255, 255) )
        my_rgb.write()
    else:
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()


# ============ Function ============

#摔倒检测
def fall_det():                      
    global lat_first, lon_first, lat_fall, lon_fall, loc_fall, status, heartbeat_Loc, des_loc
    while True:
        common()
        status = "ok"
        heartbeat_Loc = None

        if ai.get_id_data(0) and c_lock != -1:               #识别到二维码，开始充电
            switch = 0
            c_lock = -1
        
        if not ai.get_id_data(0) and c_lock == -1:         #从充电座提起断电自动记录位置——识别二维码不在就是离开出门
            rgb.fill((int(51), int(255), int(51)))         #亮一下绿灯
            rgb.write()
            time.sleep(2)
            rgb.fill((0, 0, 0))
            rgb.write()
            time.sleep_ms(1)
            c_lock = 1
            

        if c_lock == 1 and switch == 0:      #记录初始位置
            if uart1.any():
                time.sleep(0.1)
                loc_get1 = uart1.readline()              #先读取串口一行数据
                if 'GNGLL' in loc_get1:
                    location1 = (str(loc_get1).split(','))
                    if location1[2] == 'N':
                        lat_first = float(location1[1])
                    elif location1[2] == 'S':
                        lat_first = float(location1[1]) * -1
                    else:
                        lat_first = 0

                    if location1[4] == 'E':
                        lon_first = float(location1[3])
                    elif location1[4] == 'W':
                        lon_first = float(location1[3]) * -1
                    else:
                        lon_first = 0
                    des_loc = str(lon_first) + ',' + str(lat_first)
                    switch = 1             #只有读到GLL格式并存取了经纬时才记为充电结束状态
                    c_lock = 0             #只在充电一次结束的时候记录一次经纬度

        if switch == 1:
            common()
            #拐杖倒地判定
            if get_tilt_angle('X') <= 15 or get_tilt_angle('X') >= 165 or get_tilt_angle('Y') <= 110 and get_tilt_angle('Y') > 0 or get_tilt_angle('Y') >= 250 or get_tilt_angle('Z') <= -170 or get_tilt_angle('Z') >= -20:
                down = 1
            else:
                down = 0
        

            if down == 1:
                ai.picture_capture(0)                 #AI拐杖记录仪拍照
                time_on = time.time()                #记录初始时间，计时10s，10s拐杖还没起来表示老人摔倒
                my_rgb.fill( (255, 0, 0) )          #10s内先亮红灯
                my_rgb.write()
                #10s内没起来
                if time.time() - time_on > 10 and time.time() - time_on <= 30:
                    ai.picture_capture(0)
                    time.sleep_ms(100)
                    ai.picture_capture(0)
                    time.sleep_ms(100)
                    ai.picture_capture(0)
                    fall = 1
                #30s内没起来
                elif time.time() - time_on > 30:
                    ai.picture_capture(0)
                    time.sleep_ms(100)
                    ai.picture_capture(0)
                    fall = 2
            elif down == 0:
                fall = 0
        

            if fall == 1:
                if uart1.any() and c_lock == 0:            #存取倒地所在经纬度
                    time.sleep(0.1)
                    loc_get2 = uart1.readline()
                    if 'GNGLL' in loc_get2:
                        location2 = (str(loc_get2).split(','))
                        if location2[2] == 'N':
                            lat_fall = float(location2[1])
                        elif location2[2] == 'S':
                            lat_fall = float(location2[1]) * -1
                        else:
                            lat_fall = 0


                        if location2[4] == 'E':
                            lon_fall = float(location2[3])
                        elif location2[4] == 'W':
                            lon_fall = float(location2[3]) * -1
                        else:
                            lon_fall = 0

                        c_lock = 2

                loc_fall = {"latitude":lat_fall,               #修改心跳包状态
                            "longitude":lon_fall}
                status = 'emergency'
                heartbeat_Loc = loc_fall
                
                flashlight()
                music.play(music.POWER_UP, wait=False, loop=True)   #示警鸣笛声
                
            elif fall == 2:
                flashlight()
                music.play(music.POWER_UP, wait=False, loop=True)
                uart2.write('ATD' + str(user_set.get('phone')))         #倒地30s后SIM模块拨打setting中紧急联系人电话                                                     #拨打电话（SIM卡）          
            elif fall == 0:
                common()
                music.stop()

        elif switch == 0:                                   
            rgb[1] = ((int(255), int(0), int(0)))            #掌控板上自带rgb灯中间那颗亮红灯
            rgb.write()
            time.sleep_ms(1)


#"带你回家"
def get_u_home():
    global lat_now, lon_now, home_lock, loc_get3, location3##, ori_loc, des_loc, parameters
    while True:
        if p5.read_digital() == 1:                #防止老人按多次，用变量赋值
                backhome = 1

        if backhome == 1:                                                                                      #记录当前位置
            if uart1.any() and home_lock == 0:
                time.sleep(0.1)
                loc_get3 = uart1.readline()        #串口读取坐标
                if 'GNGLL' in loc_get3:            #过滤，只留GLL的格式
                    location3 = (str(loc_get3).split(','))     #存取到列表
                    #纬度存取，北正南负，赤道0°
                    if location3[2] == 'N':
                        lat_now = float(location3[1])
                    elif location3[2] == 'S':
                        lat_now = float(location3[1]) * -1
                    else:
                        lat_now = 0
                    
                    #经度存取，东正西负，否则0°
                    if location3[4] == 'E':
                        lon_now = float(location3[3])
                    elif location3[4] == 'W':
                        lon_now = float(location3[3]) * -1
                    else:
                        lon_now = 0
                    
                    home_lock = 1                              #只存取一次纬度，防止重复存取

            print(lat_now)      #电脑测试print坐标是否正确
            print(lon_now)
            #导航回家
            # ori_loc = str(lon_now) + ',' + str(lat_now)
            # parameters = 'origin='+ori_loc+'&destination='+des_loc+'&key='+key
            # route = urequests.get(url=MAP_URL+str(parameters))
            
            backhome = 0        #导航到家


#心跳包发送
def heartbeat():
    data = {                #心跳包数据存储
    "uuid": uuid,
    "status":status,
    "loc": heartbeat_Loc
    }

    resp = urequests.post(url=BASE_URL+'/heartbeat/', json=data)       #发送心跳包

    # if resp.code != 200:                    #服务器读取数据错误或无法连接
    #     print('服务器数据传输发生错误')
    #     continue

    user_set = resp.json()

    if user_set['code'] == 0:                   #返回数据类型正常
        continue
    elif user_set['code'] == 1:
        print('拐杖未注册')
        continue
    else:
        print(resp['msg'])          #查看是否正常回应


ai = NPLUS_AI()                   #小方舟初始化
ai.mode_change(1)
uart1 = machine.UART(1, baudrate=9600, tx=Pin.P14, rx=Pin.P11)
uart2 = machine.UART(2, baudrate=9600, tx=Pin.P16, rx=Pin.P15)
tim1 = Timer(1)
while True:
    tim1.init(period=5000, mode=Timer.PERIODIC, callback=heartbeat)
    common()
    fall_det()
    get_u_home()

