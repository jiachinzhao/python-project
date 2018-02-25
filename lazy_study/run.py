#encoding=utf-8
import win32com
import multiprocessing
from studybydriver import Study
from studybypost import Studybypost
import chardet
import time
import requests

from bs4 import BeautifulSoup


def worker_for_time(id, password, index=0):
    process = Study(id, password)
    process.login()
    process.study(index)
    process.driver.quit()

def worker_for_problem(id,password,index=0):
    process = Studybypost(id, password)
    process.login()
    process.study_problem(index)

def logged(id, password):
    par = {
        'email': id,
        'password': password
    }
    s = requests.Session()
    r = s.post('http://hnust.hunbys.com/index.php/home/Public/mlogin.html', data=par)
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
    process_cnt = 2
    while True:
        id = input('请输入您的学号： ')
        password = input('请输入您的密码： ')
        process_cnt = int(input('请输入所开的线程数量(默认2个,最多6个) : '))
        process_cnt = min(process_cnt, 6)
        process_cnt = max(process_cnt, 2)
        if logged(id, password):
            break
        else:
            print('登陆不成功')

    tasks = []
    print('开启{}个浏览器页面学习视频，1个后台进程提交答案'.format(process_cnt))
    try:
        tasks.append(multiprocessing.Process(target=worker_for_problem, args=(id, password, 67,)))
        for i in range(process_cnt):
            tasks.append(multiprocessing.Process(target=worker_for_time, args=(id, password, 67,)))
        for task in tasks:
            task.start()
            time.sleep(3)
        for task in tasks:
            task.join()
    except Exception as msg:
        print(msg)


