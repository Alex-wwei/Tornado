#！/usr/bin/python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import pymysql, sys
from  controllers import  home, account
# import uimethod as mt

settings = {
    "template_path":"views",
    'static_path':'statics',
    # 'static_url_prefix':'wang/',
    # 'ui_methods':mt,
}

def main():
    application = tornado.web.Application([
        (r'/', home.Chouti_handle),
        (r'/login', account.Login_handle),
        (r'/publish_art', home.Publish_handle),
        (r'/checkcode', account.Check_code_handle),
        (r'/get_mail_code', account.Mail_Check_code_handle),
        (r'/upload_file', home.upload_file_handle),
        (r'/getConmts', home.generate_conmtList_handle),
    ],  **settings)  #配置模板settings信息之后，一定要加载后面，否则没作用。
    application.listen(8081)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()