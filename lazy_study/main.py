
from selenium import webdriver


import time
import requests
import re

url1 = 'http://hnust.hunbys.com/index.php/home/Index/index.html'
base_url = 'http://hnust.hunbys.com'


class Study:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get(url1)

        time.sleep(2)
        self.driver.find_element_by_link_text('登 录').click()

        time.sleep(1)

        self.driver.find_element_by_name('email').clear()
        self.driver.find_element_by_name('email').send_keys('1405010506')

        self.driver.find_element_by_name('password').clear()
        self.driver.find_element_by_name('password').send_keys('054957')

        self.driver.find_element_by_class_name('btn-danger').click()

        time.sleep(2)

    def do_study(self):
        sample_one = '/index.php/course/Index/detail/kcid/57de44d9dfec2431775443_736/zid/57de4574cafa1521690739_736/jid/57de4ca5468e2969931802_736/nrid/57de5a8139f0a023541905_736/yulan/0.html'
        self.driver.get(base_url+sample_one)
        sample_two = '/index.php/course/Index/detail/kcid/57de44d9dfec2431775443_736/zid/57de4574cafa1521690739_736/jid/57de4ca5468e2969931802_736/nrid/57df419f49b5d592189986_736/yulan/0.html'
        time.sleep(3)
        self.driver.get(base_url+sample_two)

if __name__ == '__main__':
    process = Study()
    process.login()
    process.do_study()








