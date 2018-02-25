# coding=utf-8

import requests
import chardet
from bs4 import BeautifulSoup
from collections import defaultdict
import json

def Decode(content):
    encoding = chardet.detect(content)['encoding']
    return content.decode(encoding)


def get_train(date, from_city, to_city):
    url_huoche100 = 'http://www.chepiao100.com/yupiao/长沙,邵东,2017-04-22.html'
    from_pinyin = get_pinyin(from_city)
    to_pinyin = get_pinyin(to_city)
    if from_pinyin != None and to_pinyin != None:
        url_huochetieyou = 'http://www.tieyou.com/daigou/{}-{}.html?date={}'.format(from_pinyin, to_pinyin, date)
        s = requests.Session()
        try:
            r = s.get(url_huochetieyou)
            data = parse(Decode(r.content), date, from_city, to_city)
            return data
        except Exception as msg:
            print(msg)

def get_pinyin(city):
    with open('train_list.json', 'r') as f:
        js = json.loads(f.read())
        try:
            return js[city]
        except Exception as msg:
            return None

def rep(text):
    return text.replace('\xa0', '').replace(' ', '').replace('\n', '')

def parse(data, date, from_city, to_city):
    soup = BeautifulSoup(data, 'html.parser')
    searchList = soup.find('div', attrs={'id': 'searchList'})
    trainItems = searchList.findAll('div', attrs={'sign': 'trainItem'})
    response_js = defaultdict(list)
    response_js['error'] = 0
    for train in trainItems:
        lst_time = train.find('li', attrs={'class': 'w95 lst_time'})
        start_time = lst_time.find('strong').text

        end_time = lst_time.find('span').text
        checi = train.find(
            'li', attrs={'class': 'w95 lst_number'}).find('strong').text
        lst_place = train.find(
            'li', attrs={'class': 'w90 lst_place'}).findAll('em')
        start_log = lst_place[0]['class']
        end_log = lst_place[1]['class']
        cost_time = train.find(
            'li', attrs={'class': 'w90 lst_duration'}).text.replace('\n', '').replace(' ', '')
        lst_seat = train.find('li', attrs={'class': 'w215 lst_seat'})
        lines = lst_seat.findAll('p')
        item = defaultdict(list)
        item['startTime'] = start_time
        item['endTime'] = end_time
        item['from'] = from_city
        item['to'] = to_city
        item['duration'] = cost_time
        item['trainNo'] = checi
        for line in lines:
            seat_leave = rep(line.find('em').text)
            # print(seat_leave)
            span = line.find('span').findAll('span')
            seat_type = rep(span[0].text)
            seat_price = rep(span[1].text)
            # print(seat_type)
            item['seatInfos'].append({'seat':seat_type, 'seatPrice':seat_price,'remainNum': seat_leave})
        response_js['trainList'].append(item)
    #print(response_js)
    return response_js



if __name__ == '__main__':
    get_train('2017-04-25', "长沙", "上海")
