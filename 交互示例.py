import urequests

# heartbeat

def fall_det_thread():
    global status, heartbeat_Loc, lat_Fall, lon_fall
    while True:
        status = "ok"
        heartbeat_Loc = None
        if fall = 1:
            #获取定位
            lat_fall = ...
            lon_fall = ...
            loc_fall = {"latitude":lat_fall, 
                            "longtitude":lon_fall}
            status = "emergency"
            heartbeat_Loc = loc_fall


def heartbeat_thread():
    while True:
        BASE_URL = '127.0.0.1:8000/demoboard'

        data = {
        "uuid": uuid,
        "status": status,
        "loc": heartbeat_Loc
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