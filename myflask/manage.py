from flask_script import Manager,Shell
from myflask import app, db
from models import ACM_XTZ
import datetime

manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db,ACM_XTZ=ACM_XTZ)

manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def save():
    # user = User(2,'赵之选')
    # user.save()
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.create_all()
    log = ACM_XTZ(acmlog_datetime=time,acmlog_username='赵志轩',acmlog_title='哈哈',acmlog_content='测试')
    log.Add()

@manager.command
def query_all():
    # users = User.query_all()
    logs = ACM_XTZ.query.all()
    for log in logs:
        print(log)



if __name__ == '__main__':
    manager.run()

