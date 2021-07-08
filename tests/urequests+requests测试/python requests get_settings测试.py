import requests

# 本地
# BASE_URL = 'http://192.168.1.104:8000/demoboard'     #QFCS1
# BASE_URL = 'http://192.168.1.107:8000/demoboard'     #QFCS2
BASE_URL = 'http://192.168.31.132:8000/demoboard'    #QFCS-MI
# BASE_URL = 'http://192.168.43.199:8000/demoboard'    #idk

# 公网服务器
# BASE_URL = 'http://39.103.138.199:8000/demoboard'

# 测试uuid
uuid = 'testuuid'

# 云拐杖uuid
# uuid = 'abfb6a0d'


# http get方法
r = requests.get(url=BASE_URL+'/get_settings/'+uuid)

# 响应的内容
print(r)
print(r.json())