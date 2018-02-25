# coding=utf8

import requests

from access_token import get_access_token


def make_menu():
    access_token = get_access_token()
    post_url = ' https://api.weixin.qq.com/cgi-bin/menu/create?access_token={}'.format(access_token)
    data = {
        "button": [
            {
                "type": "click",
                "name": "今日歌曲",
                "key": "V1001_TODAY_MUSIC"
            },
            {
                "name": "菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "搜索",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "miniprogram",
                        "name": "wxa",
                        "url": "http://mp.weixin.qq.com",
                        "appid": "wx286b93c14bbf93aa",
                        "pagepath": "pages/lunar/index.html"
                    },
                    {
                        "type": "click",
                        "name": "赞一下我们",
                        "key": "V1001_GOOD"
                    }]
            }]
    }
    r = requests.post(post_url,data=data)
    print(r.text)

make_menu()