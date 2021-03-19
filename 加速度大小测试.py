#mPythonType:0
from mpython import *

import time

# 1.角度  
# 2.测试加速度大小：
#   (1)正常状态（走路或站立）：
#      x轴加速度区间[0.5429,0.8710]
#      y轴加速度区间[-0.8710,0.5703]
#      z轴加速度区间[0.1320,0.6562]

while True:
    oled.fill(0)
    x1 = accelerometer.get_x()
    y1 = accelerometer.get_y()
    z1 = accelerometer.get_z()
    oled.DispChar('加速度 x', 3, 8, 1)
    oled.DispChar((str(x1)), 52, 8, 1)
    oled.DispChar('加速度 y', 3, 24, 1)
    oled.DispChar((str(y1)), 52, 24, 1)
    oled.DispChar('加速度 z', 3, 40, 1)
    oled.DispChar((str(z1)), 52, 40, 1)
    oled.show()
    
#x1 >= 0.5429 and x1 <= 0.8710
#y1 >= -0.8710 and y1 <= 0.5703
#z1 >= 0.1320 and z1 <= 0.6562