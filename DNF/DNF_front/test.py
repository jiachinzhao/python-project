
import sys
from PyQt5.QtWidgets import QHBoxLayout,QLabel, QWidget, QApplication,QTableWidget,QTableWidgetItem
from PyQt5.QtGui import QPixmap,QBitmap,QPainter,QImage
from PyQt5.QtCore import  QByteArray
from DNF_front.ui_form import Ui_Form
from Dnf_back.dnf import DNF
import time
import threading

class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        self.islogin = -1
        self.resize(500,500)
        self.setStyleSheet("background-color:#DDDDDD")
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.thrc = None
        self.ui.lineEdit.textChanged.connect(self.logout)
        self.ui.label_3.setText('')
        self.ui.lineEdit_3.setHidden(True)
        self.ui.label_4.setHidden(True)
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pushButton_2.clicked.connect(self.scan)
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.resize(320,250)
        self.ui.tableWidget.verticalHeader().hide()
        self.dnf = DNF()
        self.show()
    def logout(self):
        print(self.islogin)
        self.islogin = -1
    def loadimage(self,imgdata):
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(imgdata))
        self.ui.label_4.setPixmap(pixmap)

    def login(self):
        print(self.islogin)
        if self.islogin == '0':
            self.setWindowTitle('您已登录')
            return
        qq = self.ui.lineEdit.text()
        if qq != self.dnf.qq:
            self.ui.label_3.setText('')
            self.ui.lineEdit_3.setHidden(True)
            self.ui.label_4.setHidden(True)
        self.dnf.qq = qq
        self.dnf.passwd = self.ui.lineEdit_2.text()
        if self.ui.lineEdit_3.isHidden():#验证码一栏初始隐藏
            if self.dnf.check_for_vcode_has():#需要验证码
                self.ui.lineEdit_3.setHidden(False)
                self.ui.label_4.setHidden(False)
                self.ui.label_3.setText('验证码')
                self.loadimage(self.dnf.imgdata)
            else:
                self.islogin =  self.dnf.submit()
                print(self.dnf.logingmessage)
                self.setWindowTitle(self.dnf.logingmessage)

        else:#需要验证码
            self.dnf.ans = self.ui.lineEdit_3.text()
            self.dnf.verify_code()
            if self.dnf.errorCode != '0':
                self.setWindowTitle('验证码不正确')
                self.dnf.check_for_vcode_has()
                self.loadimage(self.dnf.imgdata)
                return
            else:
                self.islogin = self.dnf.submit()
                self.setWindowTitle(self.dnf.logingmessage)
                if self.islogin == '0':
                    self.ui.lineEdit_3.setHidden(True)
                    self.ui.label_3.setText('')
                    self.ui.label_4.setHidden(True)
        if self.islogin == '0':
            self.dnf.driverget()


    def scan(self):
        if self.islogin != '0':
            self.setWindowTitle('您还未登录')
            return
        if self.thrc == None or  not self.thrc.is_alive():
            self.ui.tableWidget.setRowCount(0)
            time.sleep(1)
            self.thrc = threading.Thread(target=self.dnf.getinfo, args=(self,self.ui.tableWidget))  ##开辟一个接受消息的线程
            self.thrc.start()
            self.setWindowTitle('正在扫描中')
        elif not self.thrc.is_alive():
            self.ui.tableWidget.setRowCount(0)


    def closeEvent(self, QCloseEvent):
        self.dnf.driver.quit()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    Form = MainForm()
    sys.exit(app.exec())






