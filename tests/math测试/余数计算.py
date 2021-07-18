import math
import time
import keyboard

choice = 0

while True:
    if keyboard.is_pressed('space'):
        choice = (choice + 1) % 2
        print(choice)
        time.sleep(1)