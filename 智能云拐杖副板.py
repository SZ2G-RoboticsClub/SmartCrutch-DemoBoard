#1.发送提醒与定位到app上
#2.收到数字为心率
#3.与掌控板连接用socket，与app客户端用http长连接
import socket

#创建一个socket对象
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
port = 
#绑定地址
socket_server.bind((host, port))
#设置监听
socket_server.listen(5)
# socket_server.accept()返回一个元组, 元素1为客户端的socket对象, 元素2为客户端的地址(ip地址，端口号)
client_socket, address = socket_server.accept()

#while循环是为了让对话持续
while True:
	#接收客户端的请求
    recvmsg = client_socket.recv(1024)
    #把接收到的数据进行解码
    strData = recvmsg.decode("utf-8")
    #设置退出条件
    if strData == 'q':
        break
    print("接收: %s" % strData)
    #输入
    msg = input("发送: ")
    #发送数据，需要进行编码
    client_socket.send(msg.encode("utf-8"))
#关闭服务器端
socket_server.close()
