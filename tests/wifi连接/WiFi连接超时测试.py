from mpython import *
import time
import network

print('开始测试')
time.sleep(5)
print('开始连接')
time.sleep(5)

my_wifi = wifi()
my_wifi.connectWiFi('啊哈', 'dy666821')

time.sleep(5)
print('连接成功')
print(time.time())


#(自‘开始连接’开始计时)
#连接成功时间：14.81s - 5s - 5s = 4.81s
#未开WiFi连接报错时间：7.54s - 5s = 2.54s
#timeout报错时间：18.16s - 5s = 13.16s