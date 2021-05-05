import requests

r = requests.post('http://api.map.baidu.com/reverse_geocoding/v3/?ak=CZHBGZ6TXADxI2UecA1xfpq2GtKLMYam&output=json&coordtype=wgs84ll&location=31.225696563611,121.49884033194')
r = r.json()
print(r)
print(r.get('result').get('formatted_address'))