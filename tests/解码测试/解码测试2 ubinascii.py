# from mpython import *
import ubinascii

info = '深圳市第二高级中学'

loc_info = ubinascii.hexlify(info)
print("开头:" + str(loc_info), "\n", info)
print(str(loc_info))

new_info = str(loc_info).replace("b", "").replace("'", "")
print(new_info)