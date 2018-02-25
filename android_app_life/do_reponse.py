#coding=utf-8

import requests
from getinfo import get_weather,get_kuaidi
from getcity import get_city_by_ip
from get_train import get_train
class Do_Reponse:
    def __init__(self, ip, js):
        self.ip = ip
        self.js = js


    def response(self):
        type = self.js.get('type')
        if type == '1':  # 处理天气预报请求
            return self.response_weather()
        elif type == '2':
            return self.response_kuaidi()
        elif type == '3':
            return self.respone_train()
        elif type == '4':
            pass
        else:
            pass

    def response_weather(self):
        current_city = self.js.get('current_city')
        query_city = self.js.get('query_city')
        if query_city == None or query_city == '': #根据当前所在城市ip 返回天气信息
            return get_weather(current_city, current_city)
        else: #根据 查询城市 返回 天气信息
            return get_weather(query_city, current_city)


    def response_kuaidi(self):
        return get_kuaidi(self.js.get('kuaidi_id'))

    def respone_train(self):
        date = self.js.get('date')
        fromm = self.js.get('from')
        to = self.js.get('to')
        return get_train(date, fromm, to)