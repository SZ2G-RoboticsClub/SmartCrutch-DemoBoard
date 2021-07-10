# -*- coding: utf-8 -*-
# import sys
# import uuid
import requests
import hashlib
import time
# from imp import reload

# reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '219d8e0190feffd6'
APP_SECRET = 'ApRNqK0gCGMWq7t6ANTuQxLCEw3X6CJa'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect():
    global response
    q = "深圳市第二高级中学"

    data = {}
    data['to'] = 'en'
    data['from'] = 'zh-CHS'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    uuid = 'fbb72bd8'
    signStr = APP_KEY + truncate(q) + uuid + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = uuid
    data['sign'] = sign

    response = do_request(data)
    response = response.json()
    print(response)
    # contentType = response.headers['Content-Type']
    # if contentType == "audio/mp3":
    #     millis = int(round(time.time() * 1000))
    #     filePath = "合成的音频存储路径" + str(millis) + ".mp3"
    #     fo = open(filePath, 'wb')
    #     fo.write(response.content)
    #     fo.close()
    # else:
    #     print(response.content)


if __name__ == '__main__':
    connect()
    tran = response.get('translation')[0]
    print(tran)