
# -*- coding: utf-8 -*-

import socket
import sys
import threading
import time

con = threading.Condition() #互斥锁
HOST = "0.0.0.0"
PORT = 8888
data = ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
print('Socket created')
s.bind((HOST, PORT))
s.listen(10)
print ('Socket now listening')

def clientThreadIn(conn, nick):#开辟线程
    global data
    while True:#接受客户端数据
        try:
            temp = conn.recv(1024)
            if not temp:
                conn.close()#连接关闭
                print(nick.decode('utf-8'),"connection closed!")
                return
            NotifyAll(temp.decode('utf-8'))
            print(data)
        except:
            NotifyAll("server: "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' +\
            nick.decode('utf-8')+ " leaves the room!\n")
            print(data)
            return


def NotifyAll(sss):#广播
    global data
    if con.acquire():
        data = sss
        con.notifyAll()
        con.release()
 
def ClientThreadOut(conn, nick):#客户端输出
    global data
    while True:
        if con.acquire(): #获得锁
            con.wait() #阻塞自己,等待唤醒
            if data:
                try:
                    print("send data to ",nick.decode('utf-8'),":",data)
                    conn.send(data.encode('utf-8'))
                    con.release() #释放锁
                except :
                   # print("error come up:")
                    con.release()
                    return
                    

while 1:
    conn, addr = s.accept()
    print ('Connected with ' + addr[0] + ':' + str(addr[1]))
    nick = conn.recv(1024)
    NotifyAll('server: '+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' \
    'Welcome ' + nick.decode('utf-8') + ' to the room!\n')
    print(data)
    print(str((threading.activeCount() + 1) / 2) + ' person(s)!')
    conn.send(data.encode('utf-8'))
    threading.Thread(target = clientThreadIn , args = (conn, nick)).start()#开辟线程
    threading.Thread(target = ClientThreadOut , args = (conn, nick)).start()



