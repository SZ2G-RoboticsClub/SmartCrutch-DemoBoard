#mPythonType:0
from mpython import *

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