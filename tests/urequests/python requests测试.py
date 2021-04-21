import requests

uuid = '3141592653589793'


# http get方法
r = requests.get(url='http://192.168.43.199:8000/demoboard/get_settings/'+uuid)

# 响应的内容
print(r.json())