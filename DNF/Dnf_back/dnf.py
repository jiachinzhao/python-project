
from selenium import  webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PyQt5.QtWidgets import  QTableWidgetItem
import execjs
import random
import urllib
import tea
import requests, re, os, tempfile
import base64, hashlib, rsa, binascii
import simplejson
import chardet
import time
import sys
from Dnf_back import tea
class DNF(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.qq = None
        self.passwd = None
        self.verficode = None
        self.cap_cd = None
        self.sess = None
        self.vsig = None
        self.appid = '21000127'
        self.loginSig = None
        self.sess = None
        self.errorCode = None
        self.ans = None
        self.vcodeShow = 0
        self.urlgettype = 'https://ssl.captcha.qq.com/cap_union_new_gettype'
        self.urlLogin = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin'
        self.urlCheck = 'https://ssl.ptlogin2.qq.com/check'
        self.urlSig = 'https://ssl.captcha.qq.com/cap_union_new_getsig'
        self.urlgetcapbysig ='https://ssl.captcha.qq.com/cap_union_new_getcapbysig'
        self.urlverify = 'https://ssl.captcha.qq.com/cap_union_new_verify?random='
        self.urlSubmit = 'https://ssl.ptlogin2.qq.com/login'
        self.urlchecksig = None
        self.logingmessage = None
        self.imgdata = None #二进制存储验证码图片
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
        }
        self.s = requests.Session()
        self.s.headers.update(self.headers)

    def getEncryption(self):
        puk = rsa.PublicKey(int(
            'F20CE00BAE5361F8FA3AE9CEFA495362'
            'FF7DA1BA628F64A347F0A8C012BF0B25'
            '4A30CD92ABFFE7A6EE0DC424CB6166F8'
            '819EFA5BCCB20EDFB4AD02E412CCF579'
            'B1CA711D55B8B0B3AEB60153D5E0693A'
            '2A86F3167D7847A0CB8B00004716A909'
            '5D9BADC977CBB804DBDCBA6029A97108'
            '69A453F27DFDDF83C016D928B3CBF4C7',
            16
        ), 3)
        e = int(self.qq).to_bytes(8, 'big')
        o = hashlib.md5(self.passwd.encode())
        r = bytes.fromhex(o.hexdigest())
        p = hashlib.md5(r + e).hexdigest()
        a = binascii.b2a_hex(rsa.encrypt(r, puk)).decode()
        s = hex(len(a) // 2)[2:]
        l = binascii.hexlify(self.verifycode.upper().encode()).decode()
        c = hex(len(l) // 2)[2:]
        c = '0' * (4 - len(c)) + c
        s = '0' * (4 - len(s)) + s
        salt = s + a + binascii.hexlify(e).decode() + c + l

        return base64.b64encode(
            tea.encrypt(bytes.fromhex(salt), bytes.fromhex(p))
        ).decode().replace('/', '-').replace('+', '*').replace('=', '_')

    def getloginSig(self):
        par = {
            'proxy_url': 'http://game.qq.com/comm-htdocs/milo/proxy.html',
            'appid': '21000127',
            'target': 'self',
            's_url': 'http://dnf.qq.com/main.shtml',
            'style': '20',
            'daid': '8'
        }
        r = self.s.get(self.urlLogin, params=par, verify=True)
        print('提交' + self.urlLogin, '返回状态码为 :', r.status_code)
        self.loginSig = r.cookies['pt_login_sig']

    def getcap_cd(self):
        # 判断是否需要验证码
        par = {
            'regmaster': '',
            'pt_tea': '2',
            'pt_vcode': '1',
            'uin': self.qq,
            'appid': self.appid,
            'js_ver': '10197',
            'js_type': '1',
            'login_sig': self.loginSig,
            'u1': 'http://dnf.qq.com/main.shtml',
            'r': '0.6081957361829017',
            'pt_uistyle': '40'
        }
        r = self.s.get(self.urlCheck, params=par, verify=True)
        li = re.findall('\'(.*?)\'', r.text)
        print(li)
        self.vcodeShow = li[0]
        if self.vcodeShow == '1':
            self.cap_cd = li[1]  # 如果需要验证码的话  那么就是下面的cap_cd
        else:
            self.verifycode = li[1]
            self.session = li[3]

    def getsess(self):
        par = {
            'aid': self.appid,
            'asig': '',
            'captype': '',
            'protocol': 'https',
            'clientype': '2',
            'disturblevel': '',
            'apptype': '2',
            'curenv': 'inner',
            'uid': self.qq,
            'cap_cd': self.cap_cd,
            'lang': '2052',
            'callback': '_aq_363624',
        }
        r = self.s.get(self.urlgettype, params=par)
        print(r.text)
        js = simplejson.loads(r.text[11:-1])
        self.sess = js['sess']
        print(self.sess)

    def getvsig(self):
        par = {
            'asig': '',
            'disturblevel': '',
            'captype': '',
            'sess': self.sess,
            'rand': '0.5757690031634938ischartype=1',
            'uid': self.qq,
            'apptype': '2',
            'clientype': '2',
            'lang': '2052',
            'aid': self.appid,
            'rnd': '851399',
            'showtype': 'embed',
            'protocol': 'https',
            'curenv': 'inner',
            'noBorder': 'noborder',
            'cap_cd': self.cap_cd
        }
        r = self.s.get(self.urlSig, params=par)
        #print(r.request.url)
        print(r.status_code)
        print(r.text)
        self.vsig = r.json()['vsig']

    def getvcode_img(self):
        data = {
            'aid': self.appid,
            'asig': '',
            'captype': '',
            'protocol': 'https',
            'clientype': '2',
            'disturblevel': '',
            'apptype': '2',
            'curenv': 'inner',
            'sess': self.sess,
            'noBorder': 'noborder',
            'showtype': 'embed',
            'uid': self.qq,
            'cap_cd': self.cap_cd,
            'lang': '2052',
            'rnd': '851399',
            'rand': '0.21025826884257803',
            'vsig': self.vsig,
            'ischartype': '1'
        }
        r = self.s.get(self.urlgetcapbysig, params=data)
        print(r.status_code)
        self.imgdata = r.content

    def check_for_vcode_has(self):
        self.getloginSig()
        self.getcap_cd()
        if self.vcodeShow == '1':#如果需要获取验证码
            self.getsess()
            self.getvsig()
            self.getvcode_img()
            return True
        return False

    def verify_code(self):
        data = {
            'cdata': '0',
            'ans': self.ans,
            # 'collect':collect,
            'aid': self.appid,
            'asig': '',
            'captype': '',
            'protocol': 'https',
            'clientype': '2',
            'disturblevel': '',
            'apptype': '2',
            'curenv': 'inner',
            'sess': self.sess,
            'noBorder': 'noborder',
            'showtype': 'embed',
            'uid': self.qq,
            'cap_cd': self.cap_cd,
            'lang': '2052',
            'rnd': '851399',
            'subcapclass': '0',
            'vsig': self.vsig
        }
        r = self.s.post(self.urlverify + str(int(round(time.time() * 1000))), data=data)
        print(r.status_code)
        print(r.text)
        js = r.json()
        self.errorCode = js['errorCode']
        self.verifycode = js['randstr']
        self.session = js['ticket']

    def submit(self):
        par = {
            'action': '1-13-1487832712595',
            'aid': self.appid,
            'daid': 8,
            'from_ui': 1,
            'g': 1,
            'h': 1,
            'js_type': 1,
            'js_ver': 10180,
            'login_sig': self.loginSig,
            'p': self.getEncryption(),
            'pt_randsalt': 0,
            'pt_uistyle': 40,
            'pt_vcode_v1': self.vcodeShow,
            'pt_verifysession_v1': self.session,
            'ptlang': 2052,
            'ptredirect': 0,
            't': 1,
            'u': self.qq,
            'u1': 'http://dnf.qq.com/main.shtml',
            'verifycode': self.verifycode
        }
        r = self.s.get(self.urlSubmit, params=par, verify=True)
        print(r.request.url)
        print('提交账号密码返回的结果:')
        print(r.text)
        print('\n\n')
        li = re.findall('\'(.*?)\'', r.text)
        self.urlchecksig = li[2]
        self.logingmessage = li[4]
        return li[0]

    def driverget(self):
        self.driver.get(self.urlchecksig)

    def getinfo(self,Form,tableWidget):
        start = time.time()
        driver = self.driver
        locator = (By.LINK_TEXT, '切换角色 ›')
        WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located(locator))
        driver.find_element_by_link_text('切换角色 ›').click()
        # 选择大区
        element = driver.find_element_by_xpath("//select[@id='area1ContentId_DNF']")
        all_options = element.find_elements_by_tag_name('option')  # 获取所有大区的选择
        print(len(all_options))
        time.sleep(1)
        all_options[0].click()
        element = driver.find_element_by_xpath("//select[@id='area1ContentId_DNF']")
        all_options = element.find_elements_by_tag_name('option')  # 获取所有大区的选择
        print(len(all_options))
        len_daqu = len(all_options)
        for i in range(1, len_daqu):
            option = all_options[i]
            try:
                option.click()
                # 选择服务器
                element_server = driver.find_element_by_xpath("//select[@id='areaContentId_DNF']")
                server_options = element_server.find_elements_by_tag_name('option')
                server_options[0].click()
                time.sleep(0.2)
                element_server = driver.find_element_by_xpath("//select[@id='areaContentId_DNF']")
                server_options = element_server.find_elements_by_tag_name('option')
                len_server = len(server_options)
                for j in range(1, len_server):
                    option1 = server_options[j]
                    try:
                        area = option1.text
                        # print(option1.text,end=':')
                        option1.click()
                        time.sleep(0.8)
                        if driver.find_element_by_id('errorMessage_DNF').text != '在该服务器上未获取到角色信息！':
                            element_role = driver.find_element_by_xpath("//select[@id='roleContentId_DNF']")
                            if element_role:
                                role_options = element_role.find_elements_by_tag_name('option')
                                len_role = len(role_options)
                                for k in range(0, len_role):
                                    rolename = role_options[k].text
                                    rolestr = role_options[k].get_attribute('rolestr')
                                    pair = rolestr.split('&')[3].split('=')
                                    if pair[0] == 'roleLevel':
                                      try:
                                        end = tableWidget.rowCount()
                                       # print(end)
                                        tableWidget.insertRow(end)
                                        tableWidget.setItem(end, 0, QTableWidgetItem(area))
                                        tableWidget.setItem(end, 1, QTableWidgetItem(rolename))
                                        tableWidget.setItem(end, 2, QTableWidgetItem(pair[1]))
                                      except Exception as msg:
                                          print(msg)
                                          driver.delete_all_cookies()
                                          self.driverget()
                                          Form.setWindowTitle('扫描出现异常，请重现开始扫描')
                                          return

                    except Exception as msg:
                        print(msg)
                        driver.delete_all_cookies()
                        self.driverget()
                        Form.setWindowTitle('扫描出现异常，请重现开始扫描')
                        return

            except Exception as msg:
                print(msg)
                driver.delete_all_cookies()
                self.driverget()
                Form.setWindowTitle('扫描出现异常，请重现开始扫描')
                return

        Form.setWindowTitle('扫描结束耗时'+str(time.time()-start))
        driver.delete_all_cookies()
        self.driverget()