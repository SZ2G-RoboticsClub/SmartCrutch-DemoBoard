#mPythonType:0
from mpython import *
import time

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

while True:
    angle_x = get_tilt_angle('X')
    angle_y = get_tilt_angle('Y')
    angle_z = get_tilt_angle('Z')
    oled.fill(0)
    oled.DispChar('加速度角度测试：', 0, 0, 1)
    oled.DispChar(('x轴：' + str(angle_x)), 0, 16, 1)
    oled.DispChar(('y轴：' + str(angle_y)), 0, 32, 1)
    oled.DispChar(('z轴：' + str(angle_z)), 0, 48, 1)
    oled.show()
    time.sleep(0.2)