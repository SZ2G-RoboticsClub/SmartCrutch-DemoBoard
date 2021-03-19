from mpython import *
import math
import radio

radio.on()
radio.config(channel=13)
sense_pulse = radio.receive()    #只接收心率
#发送心率到app
#倒地提醒与报警拨号直接由主板发到app上