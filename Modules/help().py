from mpython import *
import music

def help():
    global freq
    oled.fill(0)
    oled.DispChar('我摔跤了，请帮帮我！', 8, 24)
    oled.show()
    for freq in range(880, 1930, 35):
        music.pitch(freq, 50)
    for freq in range(1930, 880, -35):
        music.pitch(freq, 50)


while True:
    help()