from flask import Flask,render_template,request,redirect,abort
from flask_sqlalchemy import SQLAlchemy
from urllib import parse
from hashlib import sha1
import datetime
app = Flask(__name__)
uname = ""
pwd = ""
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" + uname + ":" + pwd +  \
                                        "@localhost:3306/acmlog?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['pwd'] = 'hnust'
db = SQLAlchemy(app)



@app.route('/',methods=['GET'])
def index():
    from models import ACM_XTZ
    logs = ACM_XTZ.query.order_by(db.desc(ACM_XTZ.acmlog_id)).all()
    return render_template('index.html',logs=logs)


@app.route('/add',methods=['GET'])
def add():
    return render_template('add.html')

@app.route('/login',methods=['POST'])
def login():
    username = request.form['sendUserName']
    password = request.form['password']
    title = request.form['title']
    content = request.form['content']
    if password == app.config['pwd']:
        from models import ACM_XTZ
        log = ACM_XTZ(acmlog_datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                      acmlog_username=username,acmlog_title=title,acmlog_content=content)
        log.Add()
        return redirect('/')
    else:
        return 'the passwd is not correct'


if __name__ == "__main__":
    app.run()
