#encoding = utf-8
from flask import Flask, request, redirect, abort, make_response
from hashlib import sha1
from urllib import parse
from xml.etree import ElementTree
from time import time
app = Flask(__name__)

def handler(data):
    root = ElementTree.fromstring(data)
    ToUserName = root.find('ToUserName').text
    FromUserName = root.find('FromUserName').text
    Content = root.find('Content').text
    MsgId = root.find('MsgId').text
    CreateTime = root.find('CreateTime').text
    MsgType = root.find('MsgType').text

    print(ToUserName, FromUserName, Content, MsgId, MsgType, CreateTime)

    res = '<xml>' \
          '<ToUserName><![CDATA[{}]]></ToUserName>' \
          '<FromUserName><![CDATA[{}]]></FromUserName>' \
          '<CreateTime>{}</CreateTime>' \
          '<MsgType><![CDATA[text]]></MsgType>' \
          '<Content><![CDATA[{}]]></Content>' \
          '<MsgId>{}</MsgId></xml>'.format(FromUserName, ToUserName, int(time()), '大家好', MsgId)

    print(res)
    return res
def checksignature(query_string):
    return True
    par = dict((k, v if len(v) > 1 else v[0]) for k, v in parse.parse_qs(query_string).items())
    print(len(par))
    if len(par) < 4:
        return False
    token = 'lifeisshortlovepython'
    signature = par.get('signature')
    timestamp = par.get('timestamp')
    nonce = par.get('nonce')
    echostr = par.get('echostr')
    openid = par.get('openid')

    # print(token, timestamp, nonce)
    Arr = [token, nonce, timestamp]
    Arr.sort()
    s = ''.join(Arr)
    if sha1(s.encode('utf-8')).hexdigest() == signature:
        return True
    return False

@app.route('/weixin',methods=['GET','POST'])
def weixin():
    if checksignature(request.query_string.decode('utf-8')):
         res_data = handler(request.data)
         response = make_response(res_data)
         return response
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True, port=5050)

