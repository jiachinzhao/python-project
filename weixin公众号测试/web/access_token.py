# coding=utf8

import requests
import time

def get_access_token():
    access_token = None
    # 先在文件中查询access_token 是否超时，若没超时，直接返回，否则重新获取并更新
    with open('data/access_token', 'r', encoding='utf-8') as f:
        try:
            js_data = eval(f.read())
            if js_data.get('access_token'):
                access_token = js_data['access_token']
                his_time = int(js_data['time'])
                now_time = int(round(time.time()))
                #print(now_time - his_time)
                if now_time - his_time < 7100:
                    return access_token
                print('access_token 过期，请求新的token...')
        except Exception as msg:
            print(msg)


    with open('data/secret', 'r', encoding='utf-8') as fc:
        lines = [line for line in fc.readlines()]
        APPSECRET = lines[0].split()[1]
        APPID = lines[1].split()[1]
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'\
        .format(APPID, APPSECRET)
        r = requests.get(url)
        result = r.json()
        result['time'] = int(round(time.time()))
        with open('data/access_token', 'w', encoding='utf-8') as f:
            f.write(str(result))
        return result['access_token']

