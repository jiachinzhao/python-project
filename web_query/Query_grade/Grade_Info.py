from bs4 import  BeautifulSoup
from collections import OrderedDict


f = open('test_grade.txt','rb')
content = f.read().decode('utf-8')
soup = BeautifulSoup(content)

tr_item = soup.find_all('td',height="23")
ex = tr_item
#for x in ex:
    #print(x)
print(len(tr_item))

i = 1
all_grade = {}
mp = ['','seq','stu_id','name','date','subject','grade','space','type1','type2','stu_time','stu_grade','status','restu_time']

while i < 784:
   res = []
   for j in range(1,14):
     #print(tr_item[i+j].text,end='')
     if j == 7 and  tr_item[i+j].text.strip() =='':
         print('A','A')
     res.append((mp[j],tr_item[i+j].text.replace('\xa0','')))
     #print(tr_item[i+j].text.replace('\xa0','S').replace(' ','K'))
   js = OrderedDict(res)
  # print('')
   #print(js)
   all_grade[js['seq']] = js
   i+=14
'''
all_grade= OrderedDict(sorted(all_grade.items(),key = lambda x:int(x[0])))
print(all_grade)
for js in all_grade:
    for x in all_grade[js]:
        print(all_grade[js][x],end=' ')
    print('')
'''