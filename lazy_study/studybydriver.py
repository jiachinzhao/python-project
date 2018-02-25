#coding = utf-8

from selenium import webdriver
import time
import re
class Study:
    def __init__(self, id, password):
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.base_url = 'http://hnust.hunbys.com'
        self.url_login = '/index.php/home/Public/mlogin.html'
        self.id = id
        self.password = password

    def login(self):
        self.driver.get(self.base_url + self.url_login)

        self.driver.find_element_by_name('email').clear()
        self.driver.find_element_by_name('email').send_keys(self.id)

        self.driver.find_element_by_name('password').clear()
        self.driver.find_element_by_name('password').send_keys(self.password)

        self.driver.find_element_by_class_name('btn-danger').click()

        time.sleep(2)

    def get_mp4_link(self):
        with open('mp4_link.txt', 'r', encoding='utf-8') as f:
            link_list = []
            for line in f.readlines():
                link_list.append(line.split()[0])
            return link_list

    def get_s(self, x):
        m ,s = x.split(':')
        return int(m) * 60 + int(s)

    def study(self,index):
        i = 0
        link_list = self.get_mp4_link()
        for link in link_list:
            i += 1
            if i < index:
                continue
            try:
                self.driver.get(self.base_url+link)
                self.driver.execute_script("$('.shouke').unbind()")
                time.sleep(2)
                start_time = time.time()
                pattern1 = r'<div class=\"vjs-duration-display\".*?><span class=.*?>.*?</span>(.*?)</div>'
                pattern2 = r'<div class=\"vjs-current-time-display\".*?><span class=.*?>.*?</span>(.*?)</div>'
                duration_time = self.get_s(re.findall(pattern1, self.driver.page_source)[0])
                current_time = self.get_s(re.findall(pattern2, self.driver.page_source)[0])
                #print('当前视频时长 :' + str(duration_time))
                #print('已经播放时长 :' + str(current_time))
                delta = duration_time - current_time
                while current_time < duration_time and time.time() - start_time < delta:
                    time.sleep(5)
                    now = self.get_s(re.findall(pattern2, self.driver.page_source)[0])
                    if now != 0 and now == current_time:
                        break
                    current_time = now

            except Exception as msg:
                print(msg)   
        '''
        #link = '/index.php/course/Index/detail/kcid/57de44d9dfec2431775443_736/zid/57de45e6821f0408876689_736/jid/57de487fa8e44811150843_736.html'
        while True:
            try:
                self.driver.get(link)
                self.driver.execute_script("$('.shouke').unbind()")
                time.sleep(2)
                start_time = time.time()
                pattern1 = r'<div class=\"vjs-duration-display\".*?><span class=.*?>.*?</span>(.*?)</div>'
                pattern2 = r'<div class=\"vjs-current-time-display\".*?><span class=.*?>.*?</span>(.*?)</div>'
                duration_time = self.get_s(re.findall(pattern1, self.driver.page_source)[0])
                current_time = self.get_s(re.findall(pattern2, self.driver.page_source)[0])
                print('当前视频时长 :' + str(duration_time))
                print('已经播放时长 :' + str(current_time))
                while current_time < duration_time:
                    time.sleep(5)
                    now = self.get_s(re.findall(pattern2, self.driver.page_source)[0])
                    if now == current_time:
                        break
                    current_time = now

            except Exception as msg:
                print(msg)
            '''

if __name__ == '__main__':
    process = Study('1405010506', '054957')
    process.login()
    process.study()

