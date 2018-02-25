import pymysql
from myflask import db
# def get_conn():
#     host = '127.0.0.1'
#     port = 3306
#     db = 'test'
#     user = 'root'
#     password = 'lfstlvpy'
#     conn = pymysql.connect(host=host,port=port,db=db,user=user
#                            ,password=password,charset='utf8')
#     return conn


class ACM_XTZ(db.Model):
    __tablename__ = 'acmlog'
    acmlog_id = db.Column(db.Integer,primary_key=True)
    acmlog_datetime = db.Column(db.DateTime)
    acmlog_username = db.Column(db.String(20))
    acmlog_title = db.Column(db.String(100))
    acmlog_content = db.Column(db.Text)

    # def __init__(self,acmlog_id,acmlog_datetime,acmlog_username,acmlog_title,acmlog_content):
    #     self.acmlog_id = acmlog_id
    #     self.acmlog_datetime = acmlog_datetime
    #     self.acmlog_username = acmlog_username
    #     self.acmlog_title = acmlog_title
    #     self.acmlog_content = acmlog_content

    def __str__(self):
        return  "id:{} - datetime:{} - username:{} - title:{} - content:{}".format(self.acmlog_id,self.acmlog_datetime,self
                                                                                   .acmlog_username,self.acmlog_title,self.acmlog_content)

    def Add(self):
        db.session.add(self)
        db.session.commit()








