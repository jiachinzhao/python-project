from flask import Flask,render_template,redirect,request,g
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import  DataRequired
import requests
import chardet
import urllib.request,urllib.parse,urllib.error
import http.cookiejar
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from collections import OrderedDict
base_url = 'http://kdjw.hnust.cn/kdjw/'
vcode_url = 'verifycode.servlet'
login_url = 'Logon.do?method=logon'
get_allgrade_url  = 'xszqcjglAction.do?method=queryxscj'
headers = {
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/55.0.2883.87 Chrome/55.0.2883.87 Safari/537.36'
}
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
url = 'http://kdjw.hnust.cn/kdjw/xszqcjglAction.do?method=queryxscj'
class InfoForm(FlaskForm):
    username = StringField('请输入您的学号: ',validators=[DataRequired()])
    password = PasswordField('请输入您的密码: ',validators=[DataRequired()])
    vcode = StringField('请输入验证码: ',validators=[DataRequired()])
    submit = SubmitField('查询')

@app.route('/vcode.jpg',methods=['GET'])
def getimg():
    return open("./Test/vcode.jpg",'rb').read()

@app.route('/', methods=['GET', 'POST'])
def index():

    id = None
    password = None
    print(request.method)
    if request.method == 'GET':
        '''
        global cookie,handler,opener
        handler = urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(handler)
        img = opener.open(base_url + vcode_url)
        print(cookie)
        local = open('./Test/vcode.jpg', 'wb')
        local.write(img.read())
        local.close()
        '''

        s = requests.Session()
       # print(request.cookies)
        S[request.cookies] = s
        s.headers.update(headers)
        img = s.get(base_url+vcode_url)
        #print(s.cookies)
        local = open('./Test/vcode.jpg', 'wb')
        local.write(img.content)
        local.close()
    form = InfoForm()
    #print(request.headers)
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        vcode = form.vcode.data
        form.password.data = ''
        form.vcode.data = ''
        post_data = {
            'useDogCode': '',
            'dlfl': '0',
            'x': '28',
            'y': '7',
        }
        post_data['USERNAME'] = username
        post_data['PASSWORD'] = password
        post_data['RANDOMCODE'] = vcode
        '''
       # print(post_data)
        post_data = urlencode(post_data).encode('utf-8')
        req = urllib.request.Request(base_url + login_url, data=post_data, headers=headers)
        print(req.data)
        res = opener.open(req)

        r = opener.open(urllib.request.Request(url))
        content = r.read().decode('utf-8')
        '''
        print(request.cookies)
        s = S[request.cookies]
        #print(s)
        if s == None:
            return render_template('error.html')
        r = s.post(base_url+login_url,data = post_data)
        print(r.text)
        r = s.get(url)
        coding = chardet.detect(r.content)['encoding']
        soup = BeautifulSoup(r.content.decode(coding))
        #print(soup)
        tr_item = soup.find_all('td', height="23")
        print(len(tr_item))
        total = len(tr_item)
        if len(tr_item) != 785:
            return render_template('error.html')
        ex = tr_item
        i = 1
        all_grade = {}
        mp = ['', 'seq', 'stu_id', 'name', 'date', 'subject', 'grade', 'grade_flag', 'type1', 'type2', 'stu_time',
              'stu_grade', 'status','restu_time']
        js_total = {}
        while i < len:
            res = []
            for j in range(1, 14):
               # print(tr_item[i + j].text, end='')
                if (j == 7 or j == 13) and tr_item[i+j].text.strip() == '':
                   # print(bool(tr_item[i+j].text ==""))
                    res.append((mp[j],'无'))
                else:
                   res.append((mp[j],tr_item[i + j].text.replace('\xa0', '')))
            #print('')
            #print(js)
            js = OrderedDict(res)
            print(js)
            js_total[js['seq']] = js
            i += 14
        js_total = OrderedDict(sorted(js_total.items(),key = lambda x:int(x[0])))
        return render_template('grade.html',js = js_total)
    return render_template('index.html',form=form)

if __name__ == "__main__":
    S = {}
    manager.run()
