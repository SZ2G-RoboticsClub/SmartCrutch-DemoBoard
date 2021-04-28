import requests


BASE_URL = 'http://0.0.0.0:8000/demoboard'
uuid = '3141592653589793'

data = {                #心跳包数据存储
    "uuid": uuid,
    "status":'ok',
    "loc": None
}

r = requests.post(url=BASE_URL+'/heartbeat', json=data) 

resp = r.json()

print(resp)

# if r.code != 200:           #服务器读取数据错误或无法连接
#     print('服务器数据传输发生错误')
#     continue


# if resp['code'] == 0:                   #返回数据类型正常
#     i = 0
#     continue
# elif resp['code'] == 1:
#     print('拐杖未注册')
#     continue
# else:
#     print(resp['msg'])          #查看是否正常回应

    
