from mpython import *
import time

while True:
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()
    
    oled.fill(0)
    oled.DispChar('加速度大小测试：', 0, 0, 1)
    oled.DispChar(('x轴：' + str(x)), 0, 16, 1)
    oled.DispChar(('y轴：' + str(y)), 0, 32, 1)
    oled.DispChar(('z轴：' + str(z)), 0, 48, 1)
    oled.show()
    
    if z >= -0.5:            #究其根本
        rgb.fill((int(255), int(0), int(0)))
        rgb.write()
    else:
        rgb.fill((0, 0, 0))
        rgb.write()