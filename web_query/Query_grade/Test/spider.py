#coding = utf-8
import requests
import chardet
import urllib.request,urllib.parse,urllib.error
import http.cookiejar
from urllib.parse import urlencode
from bs4 import BeautifulSoup
Chrome_headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}
headers = {
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/55.0.2883.87 Chrome/55.0.2883.87 Safari/537.36'
}
IE_compatible_headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E)'
}
#for qurey_my_college_grade

base_url = 'http://kdjw.hnust.cn/kdjw/'
vcode_url = 'verifycode.servlet'
login_url = 'Logon.do?method=logon'
get_allgrade_url  = 'xszqcjglAction.do?method=queryxscj'
post_data = {
    'useDogCode':'',
    'dlfl':'0',
    'USERNAME':'1405010506',
    'PASSWORD':'054957',
    'x':'28',
    'y':'7',
}
s = requests.Session()
s.headers.update(headers)

r = s.get(base_url+vcode_url)
print(s.cookies)
local = open('vcode.jpg','wb')
local.write(r.content)
local.close()
vcode = input('请输入验证码:')
post_data['RANDOMCODE'] = vcode

#post_data = urlencode(post_data).encode('utf-8')
r = s.post(base_url+login_url,data=post_data)
coding = chardet.detect(r.content)['encoding']
print(coding)
print(r.content.decode(coding))

r = s.get(base_url+get_allgrade_url)
print(r.text)

'''
f = open('test_grade.html','r')
soup = BeautifulSoup(f.read(),'html.parser')
tr_item = soup.find_all('tr')
print(tr_item)
'''