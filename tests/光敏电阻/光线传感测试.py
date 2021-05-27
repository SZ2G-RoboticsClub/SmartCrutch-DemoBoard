from mpython import *

p0 = MPythonPin(0, PinMode.ANALOG)

while True:
    br = p0.read_analog()
    oled.fill(0)
    oled.DispChar(str(br), 0, 0, 1, True)
    oled.show()
    time.sleep_ms(50)