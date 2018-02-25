#coding=utf-8

import socket


def sniffer(count,bufferSize=65565,showPort=False,showRawData=False):
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP) #建立一个原始套接字，能够读取ip数据报
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    HOST = socket.gethostbyname(socket.gethostname())
    s.bind((HOST, 0))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1) #手动构造ip头部
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)#让该套接字接收所有的数据报
    for i in range(count):
            package = s.recvfrom(bufferSize)
            printPacket(package,showPort,showRawData)

def printPacket(package,showPort,showRawData):
    dataIndex = 0
    headerIndex = 1
    ipAddressIndex = 0
    portIndex = 1
    pro_map = {1:"ICMP",6:"TCP",17:"UDP"}
    data = package[0]
    print("协议: ",pro_map[data[9]])
    src = data[12:16]
    des = data[16:20]
    print("源地址: %s.%s.%s.%s"%(src[0],src[1],src[2],src[3]))
    print("目的地址: %s.%s.%s.%s" % (des[0], des[1], des[2], des[3]))
    real_data = package[dataIndex]

    print('IP:',package[headerIndex][ipAddressIndex])
    '''
    if(showPort):
        print('Port:',package[headerIndex][portIndex])
    '''
    if(showRawData):
      #print('Data: ',real_data)
      print(real_data)


if __name__ == "__main__":
    sniffer(2,2048,True,True)






