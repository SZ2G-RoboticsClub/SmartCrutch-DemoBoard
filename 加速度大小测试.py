#mPythonType:0
from mpython import *

while True:
    oled.fill(0)
    x1 = accelerometer.get_x()
    y1 = accelerometer.get_y()
    z1 = accelerometer.get_z()
    oled.DispChar('加速度 x', 3, 11, 1)
    oled.DispChar((str(x1)), 52, 11, 1)
    oled.DispChar('加速度 y', 3, 22, 1)
    oled.DispChar((str(y1)), 52, 22, 1)
    oled.DispChar('加速度 z', 3, 33, 1)
    oled.DispChar((str(z1)), 52, 33, 1)
    oled.show()