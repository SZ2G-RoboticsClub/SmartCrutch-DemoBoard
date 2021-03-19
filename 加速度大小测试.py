<<<<<<< HEAD
#mPythonType:0
=======
#mPythonType:0
>>>>>>> b5a93e3de9f91ccf53d3013dbcb0e48ec18908ca
from mpython import *

while True:
    oled.fill(0)
    x1 = accelerometer.get_x()
    y1 = accelerometer.get_y()
    z1 = accelerometer.get_z()
<<<<<<< HEAD
    oled.DispChar('加速度 x', 3, 8, 1)
    oled.DispChar((str(x1)), 52, 8, 1)
    oled.DispChar('加速度 y', 3, 24, 1)
    oled.DispChar((str(y1)), 52, 24, 1)
    oled.DispChar('加速度 z', 3, 40, 1)
    oled.DispChar((str(z1)), 52, 40, 1)
=======
    oled.DispChar('加速度 x', 3, 11, 1)
    oled.DispChar((str(x1)), 52, 11, 1)
    oled.DispChar('加速度 y', 3, 22, 1)
    oled.DispChar((str(y1)), 52, 22, 1)
    oled.DispChar('加速度 z', 3, 33, 1)
    oled.DispChar((str(z1)), 52, 33, 1)
>>>>>>> b5a93e3de9f91ccf53d3013dbcb0e48ec18908ca
    oled.show()