import requests

r = requests.get(url='https://restapi.amap.com/v3/direction/walking?origin=116.434307,39.90909&destination=116.434446,39.90816&key=10d4ac81004a9581c1d9de89eac4035b')

print(r)
print(r.json())