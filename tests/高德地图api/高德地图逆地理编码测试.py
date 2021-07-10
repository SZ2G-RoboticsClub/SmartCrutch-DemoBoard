import requests
import math


R_GEO_URL= 'http://restapi.amap.com/v3/geocode/regeo?output=json&location='
key = '10d4ac81004a9581c1d9de89eac4035b'


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
print(loc_cycle)

r_geo = requests.get(url=R_GEO_URL+loc_cycle+'&key='+key)
r_geo = r_geo.json()
print(r_geo)

loc_info = r_geo.get('regeocode').get('formatted_address')
print(loc_info)