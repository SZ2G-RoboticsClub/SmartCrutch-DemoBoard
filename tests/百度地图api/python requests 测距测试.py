import requests

D_URL = 'http://api.map.baidu.com/routematrix/v2/walking?'
ak = 'CZHBGZ6TXADxI2UecA1xfpq2GtKLMYam'

det_lat = 23.5358
det_lon = 114.1111
end_lat = 23.5558
end_lon = 114.1200

det_loc = str(det_lat)+','+str(det_lon)
end_loc = str(end_lat)+','+str(end_lon)

para2 = 'output=json&origins='+det_loc+'&destinations='+end_loc+'&ak='+ak
d = requests.get(url=D_URL+para2)
d = d.json()
print(d)