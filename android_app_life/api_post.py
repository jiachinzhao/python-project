#coding=utf-8

import requests
import time
url = 'http://101.200.55.53/android_app_life'
s = requests.Session()
def api_train(date,fromm,to):
    start_time = time.time()
    data = {
        'date': date,
        'from': fromm,
        'to': to,
        'type': '3'
    }
    r = s.post(url, data=data)
    end_time = time.time()
    print('cost time is {}'.format((end_time - start_time)))

api_train('2017-04-25', '长沙', '北京')