from mpython import *

import neopixel

my_rgb = neopixel.NeoPixel(Pin(Pin.P13), n=24, bpp=3, timing=1)

from servo import Servo

p1 = MPythonPin(1, PinMode.IN)

import time

import music

p0 = MPythonPin(0, PinMode.IN)

p15 = MPythonPin(15, PinMode.IN)

import random

def make_rainbow(_neopixel, _num, _bright, _offset):
    _rgb = ((255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,255,255), (0,0,255), (136,0,255), (255,0,0))
    for i in range(_num):
        t = 7 * i / _num
        t0 = int(t)
        r = round((_rgb[t0][0] + (t-t0)*(_rgb[t0+1][0]-_rgb[t0][0]))*_bright)>>8
        g = round((_rgb[t0][1] + (t-t0)*(_rgb[t0+1][1]-_rgb[t0][1]))*_bright)>>8
        b = round((_rgb[t0][2] + (t-t0)*(_rgb[t0+1][2]-_rgb[t0][2]))*_bright)>>8
        _neopixel[(i + _offset) % _num] = (r, g, b)

def choosing():
    global i, time1, question, answer, luck, num, stuents, question_1, answer_1, students_1, detect
    for i in range(1, 51):
        oled.fill(0)
        make_rainbow(my_rgb, 24, 50, i)
        my_rgb.write()
        time.sleep(0.1)
        luck = stuents[(random.randint(1, len(students_1) - 1))]
        oled.DispChar('幸运学生：', 20, 5, 1)
        oled.DispChar(luck, 44, 21, 1)
        oled.show()

p2 = MPythonPin(2, PinMode.IN)

p14 = MPythonPin(14, PinMode.IN)

def answering():
    global i, time1, question, answer, luck, num, stuents, question_1, answer_1, students_1, detect
    while not time.time() - time1 >= 7:
        # 答“正确”
        if p2.read_digital() == 1:
            if answer[num] == '正确':
                oled.DispChar('恭喜你，答对了！', 16, 40, 1)
                oled.show()
                my_rgb.fill( (51, 255, 51) )
                my_rgb.write()
                music.play(music.DADADADUM, wait=True, loop=False)
                time1 = 0
            else:
                oled.DispChar('答错了哟！', 34, 32, 1)
                oled.DispChar('正确答案：错误', 22, 48, 1)
                oled.show()
                my_rgb.fill( (255, 0, 0) )
                my_rgb.write()
                music.play(music.WAWAWAWAA, wait=True, loop=False)
                time1 = 0
        # 答“错误”
        if p14.read_digital() == 1:
            if answer[num] == '错误':
                oled.DispChar('恭喜你，答对了！', 16, 40, 1)
                oled.show()
                my_rgb.fill( (51, 255, 51) )
                my_rgb.write()
                music.play(music.DADADADUM, wait=True, loop=False)
                time1 = 0
            else:
                oled.DispChar('答错了哟！', 34, 32, 1)
                oled.DispChar('正确答案：正确', 22, 48, 1)
                oled.show()
                my_rgb.fill( (255, 0, 0) )
                my_rgb.write()
                music.play(music.WAWAWAWAA, wait=True, loop=False)
                time1 = 0
    if time.time() - time1 == 7:
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        oled.DispChar('时间到！', 40, 32, 1)
        oled.DispChar(str('正确答案为：') + str(answer[num]), 22, 48, 1)
        oled.show()
        music.play(music.WAWAWAWAA, wait=True, loop=False)

def blingbling():
    global i, time1, question, answer, luck, num, stuents, question_1, answer_1, students_1, detect
    for count in range(3):
        my_rgb.fill( (255, 204, 0) )
        my_rgb.write()
        time.sleep(0.5)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        time.sleep(0.5)

servo_16 = Servo(16, min_us=750, max_us=2250, actuation_range=180)

random.seed(time.ticks_cpu())
oled.fill(0)
my_rgb.fill( (0, 0, 0) )
my_rgb.write()
servo_16.write_angle(100)
question = ['范宽以山水画闻名', '范仲淹为唐宋八大家之一', '甲骨文最早出现在商朝', '欧阳修,字永叔,号香山居士', '工蜂为雌性', '葡萄糖可水解为单糖', '白求恩为加拿大人', '海龟平时为雄性,晒太阳时会变为雌性', '集合三大性质为确定性,互一性,无序性', '生活中常说的自由落体运动的物体仅受重力']
answer = ['正确', '错误', '正确', '错误', '正确', '错误', '正确', '正确', '错误', '错误']
stuents = ['丁毅', '李骏鹏', '杨家平', '秦峰', '王安邦', '周国庆', '冼冰原', '杨家平', '钟意', '梁瑞麒', '皇甫宇骏', '罗芳', '吴瑧', '彭开源', '叶浩祺', '周奕', '罗大智']
question_1 = tuple(question)
answer_1 = tuple(answer)
students_1 = tuple(stuents)
while True:
    oled.fill(0)
    oled.DispChar('教室魔盒', 40, 24, 1)
    oled.show()
    # 抽签开始
    if p1.read_digital() == 1:
        oled.fill(0)
        oled.DispChar('开始抽取幸运儿！', 16, 24, 1)
        oled.show()
        time.sleep(1)
        music.play(music.CHASE, wait=False, loop=True)
        choosing()
        oled.DispChar(str('恭喜') + str(str(luck) + str('同学！')), 0, 45, 1)
        oled.show()
        music.stop()
        servo_16.write_angle(10)
        music.play(music.DADADADUM, wait=False, loop=False)
        blingbling()
        my_rgb.fill( (255, 204, 0) )
        my_rgb.write()
        time.sleep(2)
        servo_16.write_angle(100)
        my_rgb.fill( (0, 0, 0) )
        my_rgb.write()
        oled.fill(0)
    # 答题开始
    if p0.read_digital() == 1:
        time1 = 0
        oled.fill(0)
        oled.DispChar('进入答题模式！', 22, 24, 1)
        oled.show()
        music.play(music.ENTERTAINER, wait=True, loop=False)
        # 答题结束
        while not p15.read_digital() == 1:
            oled.fill(0)
            num = random.randint(0, len(question_1) - 1)
            detect = question[num]
            if len(detect) > 11:
                oled.DispChar(detect[0:11], 0, 0, 1)
                oled.DispChar(detect[11:], 0, 16, 1)
                oled.show()
            else:
                oled.DispChar(question[num], 0, 0, 1)
                oled.show()
            time1 = time.time()
            make_rainbow(my_rgb, 24, 50, 0)
            my_rgb.write()
            answering()
            time.sleep(3)
        oled.fill(0)
        oled.DispChar('退出答题模式！', 22, 24, 1)
        oled.show()
        blingbling()
        oled.fill(0)
