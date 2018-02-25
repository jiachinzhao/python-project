import multiprocessing
import threading
from studybypost import Studybypost
import chardet
import time
import requests
import sys
from bs4 import BeautifulSoup


def worker_for_mp4(id, password, time_interval):
    process = Studybypost(id, password)
    process.login()
    process.study_mp4(5, time_interval)


def worker_for_problem(id, password):
    process = Studybypost(id, password)
    process.login()
    process.study_problem()


def logged(id, password):
    par = {
        'email': id,
        'password': password
    }
    s = requests.Session()
    r = s.post(
        'http://hnust.hunbys.com/index.php/home/Public/mlogin.html', data=par)
    content = r.content.decode(chardet.detect(r.content)['encoding'])
    soup = BeautifulSoup(content, 'html.parser')
    error = soup.find('p', attrs={'class': 'error'})
    if error:
        print(error.text)
        return False
    success = soup.find('p', attrs={'class': 'success'})
    print(success.text)
    return True

if __name__ == '__main__':
    multiprocessing.freeze_support()
    start = time.time()
    process_cnt = 5
    while True:
        id = input('请输入您的学号： ')
        password = input('请输入您的密码： ')
        process_cnt = int(input('请输入所开的进程数量(最多10个) : '))
        process_cnt = min(process_cnt, 10)
        if logged(id, password):
            break
        else:
            print('登陆不成功')

    tasks = []
    print('开启{}个线程提交视频时间，1个进程提交答案'.format(process_cnt))
    try:
         tasks.append(multiprocessing.Process(target=worker_for_problem,args=(id,password)))

         for i in range(process_cnt):
             tasks.append(threading.Thread(target=worker_for_mp4, args=(id,password, 120)))
         for task in tasks:
             task.start()
         for task in tasks:
             task.join()
    except Exception as msg:
        print(msg)

