#encoding:utf-8
import datetime, time, re, json
from urllib import request

# print(datetime.time, datetime.datetime, datetime.date, time.clock(), time.time(), time.ctime(), time.gmtime().tostring,time.localtime())

s = re.findall(r'\d+', '123k3k45k12345k34-----6-43-6-4--74')
# s1 = re.finditer(r'\d+', '123k3k45k12345k34-----6-43-6-4--74')
s2 = re.search(r'\d+', '123k3k45k12345k34-----6-43-6-4--74')
s3 = re.match(r'\d+', '123k3k45k12345k34-----6-43-6-4--74')
s4 = re.fullmatch(r'\d+', '123k3k45k12345k34-----6-43-6-4--74')
r = '1[3,5,8]\d{3}'
n = re.match(r, '1573418723')
n1 = re.findall(r, '15734j15834')
'skd'.find('k')
# print(s, s2, s3, s4, n, n1, 'skd'.find('ked'))
# http//:www.uc123.com
# bd = request.urlopen('https://www.itheima.com', timeout=4)
# print(bd.read().decode())
# body = bd.read().decode()
# print('-----------',re.findall(r'<title>(.+?)</title>', body),'------------')
# print('-----------',re.findall(r'name="description" content="(.+?)">?', body),'------------')

list = []
for i in range(0, 5):
    for j in range(1, 4):
        if j == i:
            list.append(j)
            break
    list.append(i)

print(list)#0,1,,2,3,4,5