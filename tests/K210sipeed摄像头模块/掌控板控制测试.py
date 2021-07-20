from mpython import *
from ai import *
import time

p5 = MPythonPin(5, PinMode.IN)
i = 0

print("开始")

# ai = NPLUS_AI()
while True:
    i += 1
    print('no', i)
    if i >= 100000:
        break
    
    if p5.read_digital() == 1:
        print('start')
        ai = NPLUS_AI()
        print('ok')
        
        ai.AI_WaitForARP(0x34,[0])
        print('前摄像头准备开始')
        ai.video_capture(5)
        print('前摄像头已录制')
        
        time.sleep(7)
        
        ai.AI_WaitForARP(0x34,[1])
        print('后摄像头准备开始')
        ai.video_capture(5)
        print('后摄像头已录制')
        
        break
        
        