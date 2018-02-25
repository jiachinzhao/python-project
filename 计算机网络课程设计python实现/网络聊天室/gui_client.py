#coding=utf-8
import datetime
import time
import socket
import threading
import sys
from PyQt5.QtCore import Qt
from  PyQt5.QtWidgets import (QWidget,QLCDNumber,QSlider,
QVBoxLayout,QApplication,QMessageBox)
from PyQt5.QtGui import QTextCursor
from ui_form import Ui_Form
from Login import Login_Ui_Form
global s
recvmsg = ''
toserver_data = ''
send_failed_times = 0
class Login(QWidget):
    def __init__(self):
        super(Login,self).__init__()
        self.ui = Login_Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.showMain)
    def showMain(self):
        self.hide()
        user = self.ui.lineEdit.text()
        print(user)
        global  s
        s = Connect(user)
        main = Main(user)
        main.show()

class Main(QWidget):

    def __init__(self,user):
        super(Main, self).__init__()

        #build ui
        self.user = user
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        #connect singals
        self.ui.pushButton.clicked.connect(self.updateUi)
        self.ui.textBrowser.cursorPositionChanged.connect(self.autoScroll)
        thrc = threading.Thread(target=self.recvmessage, args=(s,))  ##开辟一个接受消息的线程
        thrc.start()

    def updateUi(self):
        global  toserver_data,send_failed_times
        msgcontent = self.user + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
        message = self.ui.textEdit.toPlainText()
        if len(message) == 0:
          QMessageBox.warning(self,"警告","发送内容不能为空,请重新输入",QMessageBox.Ok)
          return
        toserver_data = (msgcontent + message).encode('utf-8')
        try:
            s.send(toserver_data)
            self.ui.textBrowser.append(msgcontent+message)
            self.ui.textEdit.setPlainText('')
            send_failed_times = 0
        except socket.error as msg:
            send_failed_times += 1
            if send_failed_times < 3:
                print("发送消息失败，请重新发送")
            else:
                print("与服务器断开连接")
    def autoScroll(self):
        cursor = self.ui.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.ui.textBrowser.setTextCursor(cursor)
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Return and QKeyEvent.modifiers() == Qt.ControlModifier:
            self.updateUi()

    def recvmessage(self,s):
        global  recvmsg
        while True:
            recvmsg = s.recv(1024)
            if not recvmsg:
                break
            try:
                if recvmsg != toserver_data:
                    self.ui.textBrowser.append(recvmsg.decode('utf-8'))
            except:
                break
    def closeEvent(self, QCloseEvent):
        self.thrc.stop()
        s.close()

def Connect(user,ip="101.200.55.53",port=8888):
    try:
        s = socket.socket()
    except socket.error as msg:
        print("create socket failed", msg)
    print("create socket success!")
    connect_times = 0
    while True:
        try:
            s.connect((ip, port))
            s.send(user.encode('utf-8'))
            print("connected success!")
            break
        except socket.error as msg:
            connect_times += 1
            print("reconnected...", msg)
        if connect_times > 5:
            print("connected failed!")
            sys.exit()
    return s
if __name__ == "__main__":

    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec())
