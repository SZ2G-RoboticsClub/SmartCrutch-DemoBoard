from mpython import *
from ai import *
import time
# import sensor

p5 = MPythonPin(5, PinMode.IN)
i = 0

while True:
    i += 1
    print('no', i)
    if i >= 100000:
        break
    
    if p5.read_digital() == 1:
        print('start')
        ai = NPLUS_AI()
        print('ok')
        
        sensor.reset(choice=1)
        sensor.reset(choice=2)
        
        print('okk')
        
        ai.AI_WaitForARP(0x34,[0])
        print('前摄像头准备开始')
        ai.video_capture(10)
        print('前摄像头已录制')
        
        time.sleep(2)
        
        ai.AI_WaitForARP(0x34,[1])
        print('后摄像头准备开始')
        ai.video_capture(10)
        print('后摄像头已录制')
        
        i = 0
        
        