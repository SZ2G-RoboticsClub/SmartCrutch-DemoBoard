import requests
import math

CONV_URL = 'http://api.map.baidu.com/geoconv/v1/?coords='
ak = 'CZHBGZ6TXADxI2UecA1xfpq2GtKLMYam'

m = '$GNGLL,2234.41586,N,11356.00044,E,051136.000,A,A*4E'
location1 = m.split(',')

if location1[2] == 'N':
    a1 = list(str(location1[1]))
    b1 = float(''.join(a1[2:]))
    c1 = ((100 - 0) / (60 - 0)) * (b1 - 0) + 0
    lat_now = math.floor(float(location1[1]) * 0.01) + c1 * 0.01
elif location1[2] == 'S':
    a1 = list(str(location1[1]))
    b1 = float(''.join(a1[2:]))
    c1 = ((100 - 0) / (60 - 0)) * (b1 - 0) + 0
    lat_now = math.floor(float(location1[1]) * 0.01 * -1) + c1 * 0.01
else:
    lat_now = 0


if location1[4] == 'E':
    a2 = list(str(location1[3]))
    b2 = float(''.join(a2[3:]))
    c2 = ((100 - 0) / (60 - 0)) * (b2 - 0) + 0
    lon_now = math.floor(float(location1[3]) * 0.01) + c2 * 0.01
elif location1[4] == 'W':
    a2 = list(str(location1[3]))
    b2 = float(''.join(a2[3:]))
    c2 = ((100 - 0) / (60 - 0)) * (b2 - 0) + 0
    lon_now = math.floor(float(location1[3]) * 0.01 * -1) + c2 * 0.01
else:
    lon_now = 0


loc_cycle = str(lon_now) + ',' + str(lat_now)

conv_loc = requests.get(url=CONV_URL+loc_cycle+'&from=3&to=5&ak='+ak)
conv_loc = conv_loc.json()
print(conv_loc)