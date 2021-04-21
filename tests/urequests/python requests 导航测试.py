import requests

MAP_URL = 'http://api.map.baidu.com/directionlite/v1/walking?'
ak = 'CZHBGZ6TXADxI2UecA1xfpq2GtKLMYam'
ori_lat = 22.3442792
ori_lon = 113.5598307
des_lat = 22.3444004
des_lon = 113.5598133
ori_loc = str(ori_lat)+','+str(ori_lon)
des_loc = str(des_lat)+','+str(des_lon)
parameters = 'origin='+ori_loc+'&destination='+des_loc+'&ak='+str(ak)

route = requests.get(url=MAP_URL+str(parameters))
route = route.json()
print(route)
print(route.get('result').get('routes')[0].get('steps'))
