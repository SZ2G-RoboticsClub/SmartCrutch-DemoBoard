# from mpython import *
import sys

str_a = '深圳市第二高级中学'
for a1,a2 in enumerate(list(str_a)):
    print(a1, a2)
    i = hex(ord(a2))
    print(i)


# b = '0x1fd2'
# print(chr(int(b, 16)))