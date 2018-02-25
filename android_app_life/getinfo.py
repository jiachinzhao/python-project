# coding=utf8

import requests
import json
from collections import defaultdict


def get_weather(city, current_city):
    s = requests.Session()
    s.headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    url = 'http://api.jirengu.com/weather.php'
    par = {
        'city': city
    }
    r = s.get(url, params=par)
    if r.status_code == 200:
        js = json.loads(r.content.decode('utf-8'))
        error = js['error']
        status = js['status']
        if error == 0 and status == 'success':
            day_weather = js['results'][0]['weather_data']
            response_js = defaultdict(list)
            response_js['error_code'] = 0
            response_js['current_city'] = current_city
            response_js['query_city'] = city
            response_js['type'] = '1'
            for x in day_weather:
                date = x['date'].replace(' ', '')
                wind_dir = x['wind'][:2]
                wind_level = x['wind'][2:]
                high_temperature, low_temperature = x['temperature'].split('~')
                low_temperature = low_temperature[:-1]
                sky_info = x['weather']
                day = defaultdict()
                day['date'] = date
                day['wind_dir'] = wind_dir
                day['wind_level'] = wind_level
                day['low_temperature'] = low_temperature
                day['high_temperature'] = high_temperature
                day['sky_info'] = sky_info
                response_js['weather'].append(day)

            print(response_js)
            return response_js


def get_kuaidi(kuaidi_id):
    s = requests.Session()
    s.headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    url_query_company = 'https://www.kuaidi100.com/autonumber/autoComNum'
    par1 = {
        'text': kuaidi_id
    }
    url_query_info = 'https://www.kuaidi100.com/query'
    r = s.get(url_query_company, params=par1)
    js = r.json()
    print(js)
    if len(js['auto']) > 0:
        type = js['auto'][0]['comCode']
        if type != '' and type != None:

            par2 = {
                'type': type,
                'postid': kuaidi_id,
                'temp': '0.32872304711155675',
                'id': '1',
                'valicode': ''
            }
            r = s.get(url_query_info, params=par2)
            js = r.json()
            print(js)
            if js['status'] == '200':
                js_response = defaultdict()
                js_response['error'] = 0
                js_response['type'] = '2'
                js_response['data'] = js['data']
                print(js_response)
                return js_response
    return {'error': '-1'}
if __name__ == '__main__':
    # get_weather('湖南省湘潭市')
    get_kuaidi('123456')
