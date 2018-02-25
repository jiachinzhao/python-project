#coding=utf8

import requests


def get_city_by_ip(ip):
    s = requests.Session()
    ak = 'BVnCpg0NkMeicaPcOnPBG79yVa0gzHUA'
    url = 'http://api.map.baidu.com/location/ip'
    par = {
        'ip': ip,
        'ak': ak,
        'coor': 'bd09ll'
    }
    r = s.get(url, params=par)
    js = r.json()
    print(js)
    city = js['content']['address_detail']['city']
    print(city)
    return city


#get_city_by_ip('119.39.148.243')

