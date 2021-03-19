from mpython import *
import radio

#收到‘call’表示发送提醒与定位到app上，收到数字即为心率

radio.on()
radio.config(channel=13)
sense_pulse = 0
while True:
    if radio.receive() != 'call':
        sense_pulse = radio.receive()
        #发送心率到app
    elif radio.receive() == 'call':
        #发送提醒与定位到app上
