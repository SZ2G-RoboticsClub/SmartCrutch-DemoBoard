#mPythonType:0
from nplus import *

from mpython import *

ai = K210_AI()
ai.mode_change(1)
while True:
    oled.fill(0)
    oled.DispChar('小方舟测试', 0, 0, 1)
    oled.show()
    if ai.get_id_data(0):
        oled.fill(0)
        oled.DispChar('守护者云拐杖', 18, 16, 1)
        oled.DispChar('充电中', 40, 32, 1, True)
        oled.show()