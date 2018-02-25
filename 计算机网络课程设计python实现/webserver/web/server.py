#coding = utf-8

import sys
import threading
import time
import re
import socket
from  PyQt5.QtWidgets import (QWidget, QApplication,QMessageBox)
from  PyQt5.QtGui import QTextCursor
from webserver_ui import Ui_Form

class Main(QWidget):
    port = ''
    inflow = 0
    outflow = 0
    server_on = False
    def __init__(self):
        super(Main, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.closeEvent)
        self.ui.pushButton.clicked.connect(self.start)
        self.ui.textBrowser.cursorPositionChanged.connect(self.autoScroll)
    def start(self):
        self.port = self.ui.textEdit.toPlainText()
        if len(self.port) == 0:
            QMessageBox.warning(self, "警告", "端口号不能为空,请重新输入", QMessageBox.Ok)
            return
        otherthing = re.findall(r'\D',self.port)
        if len(otherthing) != 0:
            QMessageBox.warning(self, "警告", "端口号只能为数字,请重新输入", QMessageBox.Ok)
            return
        if len(self.port) < 4 or len(self.port) > 5 or int(self.port) > 65535:
            QMessageBox.warning(self, "警告", "端口号只能在1000到65535之间,请重新输入", QMessageBox.Ok)
            return
        if self.server_on == False:
            self.thrc = threading.Thread(target=start_server,args=(int(self.port),)).start()
            self.server_on = True
        else:
            QMessageBox.warning(self, "警告", "服务器已经开启", QMessageBox.Ok)

    def autoScroll(self):
            cursor = self.ui.textBrowser.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.ui.textBrowser.setTextCursor(cursor)
    def closeEvent(self, QCloseEvent):
        self.thrc.stop()
        self.close()


def start_server(port):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen(10)
    print("listening...")
    main.ui.textBrowser.append("Serving HTTP on 0.0.0.0 port "+str(port))
    main.autoScroll()
    while True:
        sockfd, addr = s.accept()
        client = do_client(sockfd, addr)
        client.start()
        time.sleep(0.3)


class do_client(threading.Thread):
  request_flow = 0
  send_flow = 0
  def __init__(self,sockfd,client_addr):
      super(do_client, self).__init__()
      self.sockfd = sockfd
      self.client_addr = client_addr

  def run(self):
         recv_data = self.sockfd.recv(2048).decode('utf-8').split("\r\n")
         if not recv_data:
             return
         self.request_flow = len(recv_data)

         main.inflow += self.request_flow
         print(str(main.inflow))
         main.ui.lineEdit.setText(str(main.inflow))
         print("请求方地址为: ", self.client_addr)
         print("请求的流量为: ",self.request_flow)
         main.ui.textBrowser.append("请求方地址为: "+str(self.client_addr))
         main.autoScroll()
         argc = recv_data[0].split(' ')
         #print(argc)

         if argc[0] == 'GET':
             self.do_GET(argc)
  def do_GET(self,argc):
      url = argc[1]
      #if url[-4:] == '.ico':#google 浏览器发送请求时，还会自带发送页面的图标请求，开始不会处理，后面可以处理了
         # return
     # print(url)
      file_path = root_path + url
      print("Get 地址为: "+file_path)
      main.ui.textBrowser.append("Get 地址为:"+file_path)
      main.autoScroll()
      file = open(file_path,'rb')
      content = file.read()
      file_length =len(content)
      #print(file_length)
      localtime = time.strftime("%a,%d %b %G %T ")
      send_data = ''
      send_data += 'Http/1.1 200 OK\r\n'
      send_data += 'Date: ' + localtime + 'GMT\r\n'

      send_data += 'Content-Type: ;charset=utf-8\r\n'
      send_data += 'Content-Length: ' + str(file_length)+'\r\n\r\n'
      send_data = send_data.encode('utf-8')
      send_data += content
      self.send_flow = len(send_data)
      print(send_data)
      self.sockfd.send(send_data)
      print("发送的流量为",self.send_flow)
      main.outflow += self.send_flow
      main.ui.lineEdit_2.setText(str(main.outflow))


if __name__ == "__main__":
    root_path = 'C:/Users/jiachinzhao/Desktop/py_post'
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())







