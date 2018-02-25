import requests
from bs4 import BeautifulSoup
import chardet
import threading
import multiprocessing
from collections import defaultdict
import re
import time

class Studybypost:

    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.s = requests.Session()
        self.base_url = 'http://hnust.hunbys.com'
        self.url_login = '/index.php/home/Public/mlogin.html'
        self.url_study1 = '/index.php/course/Index/detail/kcid/57de44d9dfec2431775443_736/zid/57de4574cafa1521690739_736/jid/57de4ca5468e2969931802_736.html'
        self.url_study2 = '/index.php/course/Index/detail/kcid/57de44984ca19277359237_365/zid/57de44984ee71302937157_365/jid/57de44984f1a8817758115_365.html'
        self.url_submit_time = '/index.php/home/Public/studyCount.html'
        self.url_submit_answer = '/index.php/exercises/Index/answer.html'

    def login(self):
        par = {
            'email': self.id,
            'password': self.password
        }
        r = self.s.post(self.base_url + self.url_login, data=par)
        content = r.content.decode(chardet.detect(r.content)['encoding'])
        soup = BeautifulSoup(content, 'html.parser')
        error = soup.find('p', attrs={'class': 'error'})
        if error:
            print(error.text)
            return False
        success = soup.find('p', attrs={'class': 'success'})
        print(success.text)
        return True

    def search_task_list(self):
        #r = self.s.get(self.base_url + self.url_study1)
        #with open('main.html', 'wb') as f:
           # f.write(r.content)
        with open('main.html', 'wb') as f:
            r = self.s.get(self.base_url + self.url_study2)
            f.write(r.content)

        from handle_html import handle
        handle()
        print('handle finished')

    def study_problem(self):
        print('problem study started...')
        with open('task_link.txt', 'r', encoding='utf-8') as f:
            index = 1
            for line in f.readlines():
                pair = line.split()
                url = self.base_url + pair[0]
                if url[-5] == '.':
                    try:
                        print('problem url is: ', url)
                        data, choices, problem = self.analysis_answer(url)
                        right_answer = self.submit_answer(data, choices, url)
                        print("{}  {} 's answer is {}".format(
                            index, problem, right_answer))
                    except Exception as msg:
                        print('提交习题答案出现异常，即将退出')
                        return
                index += 1
        print('problem study finished')

    def get_mp4_link(self):
        with open('mp4_link.txt', 'r', encoding='utf-8') as f:
            link_list = []
            for line in f.readlines():
                link_list.append(line.split()[0])
            return link_list

    def study_mp4(self, post_times, time_interval, tid):
        link_list = self.get_mp4_link()
        for link in link_list:
            print(link)
            try:
                for i in range(post_times):
                    real_link = self.base_url + link
                    # print(real_link)
                    if not self.Submit_time(real_link, time_interval):
                        print('the {}th times\'s thread exit unexpected:'.format(tid))
                        return
                    time.sleep(1)
                    print('the {}th times\'s post finished'.format(i + 1))
            except Exception as msg:
                print(msg)

    def analysis_mp4(self, link, stp, time):
        r = self.s.get(link)
        content = r.content
        encoding = chardet.detect(content)['encoding']
        soup = BeautifulSoup(content.decode(encoding), 'html.parser')
        data = defaultdict()
        data['stp'] = stp
        data['current_time'] = time
        data['xxkey'] = soup.find(id='xxkey')['value']
        sc = re.findall(r"data_count\['(.*?)'] = '(.*?)'",
                        soup.find('script', attrs={'defer': 'defer'}).text)
        for pair in sc:
            data[pair[0]] = pair[1]
        return data

    def Submit_time(self, link, time_interval):
        try:
            data = self.analysis_mp4(link, 0, 0)
            r = self.s.post(
                self.base_url + self.url_submit_time, data=dict(data))
           # print(r.text)
            xxkey = r.json()['xxkey']
            data['stp'] = 1
            data['current_time'] = time_interval
            data['xxkey'] = xxkey
            time.sleep(time_interval)
            r = self.s.post(
                self.base_url + self.url_submit_time, data=dict(data))
            print(r.text)
            return True
        except Exception as msg:
            print('提交视频时间出现异常')
            return False
    def analysis_answer(self, url):
        r = self.s.get(url)
        content = r.content
        encoding = chardet.detect(content)['encoding']
        soup = BeautifulSoup(content.decode(encoding), 'html.parser')
        data = defaultdict()
        sc = re.findall(r"data_count\['(.*?)'] = '(.*?)'",
                        soup.find('script', attrs={'defer': 'defer'}).text)
        for pair in sc:
            data[pair[0]] = pair[1]

        data['xt[]'] = soup.find('input', attrs={'name': 'xt[]'})['value']
        problem = soup.find('p', attrs={'class': 'break-out'}).text

        choices = soup.findAll('input', attrs={'class': 'answer-option'})

        return data, choices, problem

    def submit_answer(self, data, choices, url):
        right_answer = 'A'
        for choice in choices:
            tmp = data
            tmp[choice['name']] = choice['value']
            self.s.post(self.base_url + self.url_submit_answer, data=dict(tmp))
            if self.checkisright(url):
                return right_answer

            right_answer = chr(ord(right_answer) + 1)

    def checkisright(self, url):
        r = self.s.get(url)
        content = r.content
        encoding = chardet.detect(content)['encoding']
        soup = BeautifulSoup(content.decode(encoding), 'html.parser')
        # print(soup)
        right = soup.find('span', attrs={'class': 'zy-right'}).text
        if int(right) == 1:
            return True
        return False

    def work(self, post_times, time_interval):
        multiprocessing.freeze_support()
        is_stu_pro = str(input('是否需要提交习题答案(y/n): '))
        tasks = []
        tasks.append(multiprocessing.Process(target=self.work_mp4, args=(post_times, time_interval)))
        if is_stu_pro == 'y' or is_stu_pro == 'Y':
            tasks.append(multiprocessing.Process(target=self.study_problem, args=()))


        print('开始执行操作')
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()

    def work_mp4(self,post_times,time_interval):
        tasks = []
        for i in range(4):
            tasks.append(threading.Thread(target=self.study_mp4, args=(post_times, time_interval, i+1)))
        for i in range(4):
            tasks[i].start()
            print('the {}th thread start:'.format(i + 1))
        for task in tasks:
            task.join()


if __name__ == '__main__':

    process = Studybypost('1405010506','054957')
    process.login()
    process.search_task_list()

