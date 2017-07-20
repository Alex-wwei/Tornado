import pymysql
import  time,datetime
from models import model_DB

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine , and_, or_, any_

from backend.core import BaseHandleController

from urllib import request

# home.login_user['name'] = name
# home.login_user['pwd'] = pwd
# home.login_user['uid'] = u.uid
login_user = {}
isLogin = False
class Chouti_handle(BaseHandleController.BaseRequestHandleController):
    def get(self, *args, **kwargs):
        global isLogin
        article = []
        print(login_user, 'first')
        if len(login_user) > 0 and not isLogin:
            isLogin = True
        self.get_data_fromdb(article)
        self.render('chouti.html', user= login_user, article= article, islogin = isLogin)
    def post(self, *args, **kwargs):
        self.write('post')
    def get_data_fromdb(self, article):

        # sn = model_DB.session()
        # news = sn.query(model_DB.News, model_DB.User.username).filter(model_DB.News.user_id == model_DB.User.uid)
        # for item in news.all():
        #     article.append({'username':item[1],'title':item[0].title, 'content':item[0].content,'newstype':item[0].newstype_id, 'url':item[0].url, 'time':item[0].ctime, 'fav_count':item[0].fav_count})
        # sn.close()

        conn = pymysql.connect(host = '127.0.0.1', port= 3306, user = 'root', passwd = 'qwe', db= 'chouti_db', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        infect_lines = cursor.execute('SELECT  newsid as news_id, c.title, c.content, c.user_id, c.url, c.time, c.fav_count, c.types, user.username FROM (SELECT * FROM (SELECT news.nid as newsid, news.title,news.content, news.user_id, news.url, news.newstype_id, news.ctime as time, A.fav_count FROM news  LEFT JOIN (SELECT news_id, COUNT(user_id) as fav_count FROM favor GROUP BY news_id) as A on A.news_id = news.nid) as B LEFT JOIN newstype on B.newstype_id = newstype.nid) as c LEFT JOIN user on user.uid = c.user_id ORDER BY time desc')

        # print(cursor.fetchall())
# {'title': 'yhjkj', 'content': ',mnm,mnb', 'user_id': 5, 'url': 'nmnm,','time': datetime.datetime(2017, 5, 25, 17, 52, 12), 'fav_count': 1, 'types': '??', 'username': 'wei'},
        for item in cursor.fetchall():
            if item['fav_count']:
                fav_count = item['fav_count']
            else:
                fav_count = 0
            delta = (datetime.datetime.now().timestamp() - item['time'].timestamp())
            time_delta = time_deal(delta, item['time'])
            if isLogin:         #用户登录的数据更新
                # print('用户登录的数据更新')
                flag = False
                sn = model_DB.session()
                info = sn.query(model_DB.Favor).filter_by(news_id = item['news_id'])
                for ino in info.all():
                    print(ino, 'info--ino 用户登录的数据更新')
                    if ino.user_id == login_user['uid']:
                        flag = True
                        break
                if flag:
                    print(flag, 'flag count')
                    article.append({'info':'1', 'news_id': item['news_id'], 'username': item['username'], 'title': item['title'],'content': item['content'], 'newstype': item['types'], 'url': item['url'], 'time': time_delta,'fav_count': fav_count})
                else:
                    article.append(
                    {'info': '0', 'news_id': item['news_id'], 'username': item['username'], 'title': item['title'],
                     'content': item['content'], 'newstype': item['types'], 'url': item['url'], 'time': time_delta,
                     'fav_count': fav_count})
            else:
                print('用户wei登录的数据更新')
                article.append({'info': '0','news_id': item['news_id'], 'username': item['username'], 'title': item['title'], 'content': item['content'], 'newstype': item['types'], 'url': item['url'], 'time': time_delta, 'fav_count': fav_count})
            # print(item['time'],(datetime.datetime.now()-item['time']).seconds,'---',
            #       (datetime.datetime.utcnow()-item['time']).seconds, '...',
            #       (datetime.datetime.now().timestamp() - item['time'].timestamp()))
            #中间的UTC时间，不符合要求，第三个返回数据精确一些
        cursor.close()
        conn.close()
def time_deal(delta, dt):
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%d分钟前' % (delta // 60)
    if delta < 86400:
        return u'%d小时' % (delta // 3600) + time_deal(delta % 3600, dt)
    if delta < 604800:
        return u'%d天' % (delta // 86400) + time_deal(delta % 86400, dt)
    # dt = datetime.fromtimestamp(dt)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)

class Publish_handle(BaseHandleController.BaseRequestHandleController):
    def get(self, *args, **kwargs):
        print('Publish_handle get')
        if len(login_user) == 0:
            self.write('0')
        else:
            self.write('1')
    def post(self, *args, **kwargs):
        tag = self.get_argument('tag')

        sn = model_DB.session()
        if tag == '0':
            title = self.get_argument('title')
            content = self.get_argument('content')
            url = self.get_argument('url')
            newstype = self.get_argument('type')
            # print(title, content, url, newstype, tag)

            u = sn.query(model_DB.User).filter_by(username = login_user.get('name')).first()
            print(u, '---', 'login_user  Publish_handle')
            obj = model_DB.News(user_id = u.uid, newstype_id = newstype, title = title, url = url, content = content, fav_count = 0)
            sn.add(obj)
        elif tag == '1':
            content = self.get_argument('content')
            newstype = self.get_argument('type')

            u = sn.query(model_DB.User).filter_by(username=login_user.get('name')).first()
            obj = model_DB.News(user_id=u.uid, newstype_id=newstype, title='', url='', content=content, fav_count = 0)
            sn.add(obj)
        else:
            pass
        # sn.flush()
        # sn.refresh(obj)
        print('Publish_handle post','------')
        # article.append({'username':login_user.get('name'),'title': obj.title, 'content':obj.content, 'newstype_id':obj.newstype_id, 'url':obj.url, 'time':obj.ctime})
        sn.commit()
        sn.close()

        self.redirect('/')

class upload_file_handle(BaseHandleController.BaseRequestHandleController):
    def get(self, *args, **kwargs):
        id = self.get_argument('id')
        type = self.get_argument('type')
        sn = model_DB.session()
        if type == '1':
            sn.query(model_DB.News).filter_by(nid = id).update({'fav_count': model_DB.News.fav_count + 1})
            sn.add(model_DB.Favor(user_id = login_user['uid'], news_id = id))
        else:
            sn.query(model_DB.News).filter_by(nid = id).update({'fav_count': model_DB.News.fav_count - 1})
            # sn.commit()
            sn.query(model_DB.Favor).filter(and_(model_DB.Favor.news_id==id, login_user['uid']==model_DB.Favor.user_id)).delete()
        sn.commit()
        sn.close()

    def post(self, *args, **kwargs):
        print('post file')
        file = self.request.files['uploadfile']
        for item in file:
            print(item, '---file----')

class generate_conmtList_handle(BaseHandleController.BaseRequestHandleController):
    def get(self, *args, **kwargs):
        time.sleep(2)
        self.write('success_xoment')