# from mpython import *

a = '您家老人现在摔倒了！！请打开app以查询老人位置！'
uni = a.encode('unicode-escape')
print(uni)  
print(type(uni))

uni = uni.decode()
print(uni)
print(type(uni))
