# coding = utf-8

from selenium import webdriver
import time
import re


class Study:
    def __init__(self, id, password):
        self.driver = webdriver.Chrome()
        self.base_url = 'http://hnust.hunbys.com'
        self.url_login = '/index.php/home/Public/mlogin.html'
        self.url_continue_study = '/index.php/course/Index/index/kcid/57de44d9dfec2431775443_736.html'
        self.id = id
        self.password = password

    def login(self):
        print('开始登录')
        self.driver.get(self.base_url + self.url_login)

        self.driver.find_element_by_name('email').clear()
        self.driver.find_element_by_name('email').send_keys(self.id)

        self.driver.find_element_by_name('password').clear()
        self.driver.find_element_by_name('password').send_keys(self.password)

        self.driver.find_element_by_class_name('btn-danger').click()

        time.sleep(2)
        print('登陆成功')

    def get_mp4_link(self):
        with open('mp4_link.txt', 'r', encoding='utf-8') as f:
            link_list = []
            for line in f.readlines():
                link_list.append(line.split()[0])
            return link_list

    def get_s(self, x):
        m, s = x.split(':')
        return int(m) * 60 + int(s)

    def study(self):
        try:
            self.driver.get(self.base_url + self.url_continue_study)
            self.driver.find_element_by_link_text('继续学习').click()
            while True:
                try:
                    self.driver.execute_script("$('.shouke').unbind()")
                    if self.check_type() == 'mp4':
                        finished = self.handle_mp4()
                    else:
                        finished = self.handle_problem()
                    if finished:

                    else:
                        break
                except Exception as msg:
                    print(msg)
        except Exception as msg:
            print(msg)

    def check_type(self):
        x = self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[1]').text
        if x.find('.mp4') != -1:
            return 'mp4'
        return 'problem'

    def handle_mp4(self):
        try:
            time.sleep(2)
            pattern1 = r'<div class=\"vjs-duration-display\".*?><span class=.*?>.*?</span>(.*?)</div>'
            pattern2 = r'<div class=\"vjs-current-time-display\".*?><span class=.*?>.*?</span>(.*?)</div>'
            duration_time = self.get_s(re.findall(pattern1, self.driver.page_source)[0])
            current_time = self.get_s(re.findall(pattern2, self.driver.page_source)[0])
            delta = duration_time - current_time
            print('当前视频时长 :' + str(duration_time))
            print('已经播放时长 :' + str(current_time))
            start = time.time()
            while current_time < duration_time and time.time() - start < delta:
                time.sleep(5)
                print(current_time)
                now = self.get_s(re.findall(pattern2, self.driver.page_source)[0])
                if now == current_time:
                    break
                current_time = now
            return True
        except Exception as msg:
            print(msg)
        return False

    def handle_problem(self):
        x = 65
        ans_list = self.driver.find_elements_by_class_name('answer-option')
        ans_list[0].cilck()
        self.driver.execute_script('doAnswer()')
        right_answer = self.driver.find_element_by_xpath('//*[@id="zy-exercises-answer"]/ul/li/div[4]/strong').text
        index = ord(right_answer) - x
        if index == 0:
            return True
        self.driver.find_element_by_xpath('//*[@id="zy-exercises-answer"]/div[2]/a').click()
        ans_list = self.driver.find_elements_by_class_name('answer-option')
        ans_list[index].click()
        self.driver.execute_script('doAnswer()')

        right_answer = self.driver.find_element_by_xpath('//*[@id="zy-exercises-answer"]/ul/li/div[4]/strong').text
        if index == ord(right_answer) - x:
            return True
        return False


if __name__ == '__main__':
    process = Study('1405010506', '054957')
    process.login()
    process.study()

