import requests

#路径规划初始化
GEO_URL = 'https://restapi.amap.com/v3/geocode/geo?address='
key = '10d4ac81004a9581c1d9de89eac4035b'

home = '广东省深圳市罗湖区泥岗西路1068号'
h = requests.get(url=GEO_URL+home+'&output=json&key='+key)

h = h.json()
print(h)

home_loc = h.get('geocodes')[0].get('location')
# .get('0')

print(home_loc)