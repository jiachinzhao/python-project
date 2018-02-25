#coding=utf-8
import platform
import sys
import os
import time
import threading
import re

con = threading.Condition()
def get_os():
    '''''
    get os 类型
    '''
    os = platform.system()
    if os == "Windows":
        return "n"
    else:
        return "c"


def ping_ip(ip_str):
    if con.acquire():
        con.notifyAll()
        cmd = ["ping", "-{op}".format(op=get_os()),
               "1", ip_str]
        output = os.popen(" ".join(cmd)).readlines()
        flag = False
        for line in list(output):
            if not line:
                continue
            if str(line).upper().find("TTL") >= 0:
                flag = True
                break
        if flag:
            print( "ip: %s is ok ***" % ip_str)
            cmd = "arp -a "+ip_str
            output = os.popen(cmd).read()
            subp ='[a-zA-Z0-9]{2,2}:'
            pattern = subp*6
            pattern = pattern[:-1]
            mac = re.findall(pattern,output)
            if len(mac) != 0:
                print("Mac address is :"+ str(mac))
            else:
                print("Mac address cannot find!")
        else:
            print("ip : %s is unreachable ***" % ip_str)
        con.release()

def find_ip(ip_prefix):
    for i in range(1,255):
        ip = '%s.%s' % (ip_prefix, i)
        threading.Thread(target=ping_ip,args = (ip,)).start()
        time.sleep(0.3)

if __name__ == "__main__":
    print("start time %s" % time.ctime())
   # commandargs = sys.argv[1:]
   # args = "".join(commandargs)

   # ip_prefix = '.'.join(args.split('.')[:-1])
    ip_prefix = '192.168.2'
    find_ip(ip_prefix)
    print("end time %s" % time.ctime())