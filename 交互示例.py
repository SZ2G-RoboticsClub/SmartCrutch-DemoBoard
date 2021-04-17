import requests

BASE_URL = 'http://0.0.0.0:8000/demoboard'
uuid = '3141592653589793'

#获得settingdata

s = requests.get(url=BASE_URL+'/get_settings/'+uuid)

print(s.json())
