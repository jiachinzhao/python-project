# coding=utf8

from flask import Flask, request, jsonify,make_response
from do_reponse import Do_Reponse
import json
app = Flask(__name__)
@app.route('/android_app_life',methods=['GET','POST'])

def index():
    ip = get_ip()
    form = request.form
    do_res = Do_Reponse(ip, form)
    response =  make_response(jsonify(do_res.response()))
    response.headers['Access-Control-Allow-Origin'] = '*' #保证ajax的请求可以跨域
    return response


def get_ip():
    ip = request.remote_addr
    try:
        _ip = request.headers['X-Real-IP']
        if _ip is not None:
            ip = _ip
    except Exception as msg:
        print(msg)
    return ip

if __name__ == '__main__':
    app.run(port=5050, debug=True)
