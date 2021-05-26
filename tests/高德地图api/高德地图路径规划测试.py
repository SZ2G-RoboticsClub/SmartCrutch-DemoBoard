import requests

r = requests.get(url='https://restapi.amap.com/v3/direction/walking?origin=113.9375,22.57033&destination=113.931577,22.487280&key=10d4ac81004a9581c1d9de89eac4035b')

print(r)
print(r.json())