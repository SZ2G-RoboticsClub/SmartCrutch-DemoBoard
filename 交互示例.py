import urequests

# heartbeat

def thread():

    while True:

        BASE_URL = '127.0.0.1:8000/demoboard'

        data = {
        "uuid": uuid,
        "status": status,
        "loc": {
            "latitude": 0,
            "longitude": 0
        }

        resp = urequests.post(url=BASE_URL+'/heartbeat/', data=data)

        if resp.code != 200:
            print()
            continue

        resp = resp.json()

        if resp['code'] == 0:
            continue
        elif resp['code'] == 1:
            ...
        else:
            print(resp['msg'])