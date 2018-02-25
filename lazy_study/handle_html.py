
import re
import chardet
from bs4 import BeautifulSoup
from collections import defaultdict

def handle():
    with open('main.html', 'rb') as f:
        with open('task_link.txt', 'wb') as fp:
            with open('mp4_link.txt', 'wb') as fm:
                content = f.read()
                encoding = chardet.detect(content)['encoding']
                soup = BeautifulSoup(content.decode(encoding), 'html.parser')
                lists = soup.findAll('div', attrs={'class': 'panel_hr'})
                for list in lists:
                    title = list.find('a', attrs={'data-toggle': 'collapse'})['title']
                    if title.find('必修') != -1:
                        uls = list.findAll('ul', 'panel-body')
                        for ul in uls:
                            tasks = ul.findAll('a')
                            for task in tasks:
                                if task.text.split()[-1].find('.mp4') == -1:
                                    fp.write((task['href'] + ' ' + task.text + '\n').encode('utf-8'))
                                else:
                                    fm.write((task['href'] + ' ' + task.text + '\n').encode('utf-8'))


def find():
    with open('test.html', 'rb') as f:
        content = f.read()
        encoding = chardet.detect(content)['encoding']
        soup = BeautifulSoup(content.decode(encoding), 'html.parser')
        '''
        sc = re.findall(r"data_count\['(.*?)'] = '(.*?)'",soup.find('script',attrs={'defer':'defer'}).text)
        data = defaultdict()
        for pair in sc:
            data[pair[0]] = pair[1]
        print(dict(data))
        lists = soup.findAll('div', attrs={'class': 'panel_hr'})
        for list in lists:
            title = list.find('a', attrs={'data-toggle': 'collapse'})['title']
            if title.find('必修') != -1:
                uls = list.findAll('ul','panel-body')
                for ul in uls:
                    tasks = ul.findAll('a')
                    for task in tasks:
                        if task.text.split()[-1].find('.mp4') == -1:
                            fp.write((task['href'] + ' ' + task.text + '\n').encode('utf-8'))
                        else:
                            fm.write((task['href'] + ' ' + task.text + '\n').encode('utf-8'))
        '''


#handle()
#find()

