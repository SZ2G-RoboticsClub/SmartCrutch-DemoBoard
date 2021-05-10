import requests

GEO_URL = 'http://api.map.baidu.com/geocoding/v3/?address='
ak = 'CZHBGZ6TXADxI2UecA1xfpq2GtKLMYam'

home = '中国广东省深圳市南山区西丽街道留仙洞万科云城一期8栋'
r = requests.get(url=GEO_URL+home+'&output=json&ak='+ak)
print(GEO_URL+home+'&output=json&ak='+ak)
print(r)
# m = str(r).replace('showLocation&&showLocation(', '').replace(')', '')
# print(m)
a = r.json()
print(a)