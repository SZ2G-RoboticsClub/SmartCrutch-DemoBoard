import requests

uuid = 'testuuid'


# http get方法
r = requests.get(url='http://39.103.138.199:5283/demoboard/get_settings/'+uuid)

# 响应的内容
print(r)
print(r.json())