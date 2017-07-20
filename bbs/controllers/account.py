import pymysql

from backend.core import BaseHandleController
from controllers import home
from models import model_DB
from sqlalchemy import  or_
import re, random
import smtplib  #加载smtplib模块
from email.mime.text import MIMEText
from email.utils import formataddr

mail_code = None
check_code_regist = None
class Check_code_handle(BaseHandleController.BaseRequestHandleController):
    def get(self, *args, **kwargs):
        global check_code_regist
        import io
        from backend.utils import image
        mstream = io.BytesIO()

        vc = image.VerifyCode()
        img, code = vc.createCodeImage(img_type='GIF')
        img.save(mstream, 'GIF')

        check_code_regist = str(code)
        print(check_code_regist, 'check_code_regist')
        self.write(mstream.getvalue())

def sendmail(address, content, subject= '抽屉新热搜-用户注册邮箱验证'):
    ret = True

    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr(["抽屉新热搜", 'hcuwangwei@163.com'])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["star", address])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = subject  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP("smtp.163.com", 25)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login('hcuwangwei@163.com', "hcuwangwei123")  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail('hcuwangwei@163.com', [address, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件

        server.quit()  # 这句是关闭连接的意思
    except Exception as e:  # 如果try中的语句没有执行，则会执行下面的ret=False
        print(e)
        ret = False

    return ret

class Mail_Check_code_handle(BaseHandleController.BaseRequestHandleController):
    def get(self, *args, **kwargs):
        global mail_code
        print('Mail_Check_code_handle')
        mail_addr = self.get_argument('mail')
        mail_code = random.randint(100000, 999999)
        flag = sendmail(mail_addr, str(mail_code))
        if flag:
            self.write('success')
        else:
            self.write('error')


class Login_handle(BaseHandleController.BaseRequestHandleController):
    def post(self, *args, **kwargs):
        global isLogin
        name = self.get_argument('username')
        pwd = self.get_argument('pwd')
        code = self.get_argument('check_code')

        mail_REGULAR = "^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"
        result = re.match(mail_REGULAR, name)
        print(code, '----', check_code_regist)

        if code.lower() == check_code_regist.lower():
            if result:#说明是邮箱登录

                flag = self.check_user(name, pwd, 0)
            else:
                flag = self.check_user(name, pwd, 1)
            if flag:
                print('login success')
                sn = model_DB.session()
                u = sn.query(model_DB.User).filter(model_DB.User.username == name).first()
                isLogin = True
                home.login_user['name'] = name
                home.login_user['pwd'] = pwd
                home.login_user['uid'] = u.uid
                self.redirect(r'/')
            else:
                print('login error')
                self.write('error')
        else:
            self.write('code')

    def get(self, *args, **kwargs):
        name = self.get_argument('username')
        mail = self.get_argument('mail')
        pwd = self.get_argument('pwd')
        code = self.get_argument('check_code')
        mail_REGULAR = "^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"
        result = re.match(mail_REGULAR, mail)
        # and code == str(mail_code)
        if result:  # 说明邮箱格式正确
            if self.check_user(name, 'check_repeat', 1):
                self.write('repeat')
            else:
                if self.write_user_intodb(name, mail, pwd):
                    home.isLogin = True
                    home.login_user = {'name':name}
                    print('regist success')
                    self.write('success')
                else:
                    self.write('error')
        else:
            self.write('mail_or_code_error')

    def write_user_intodb(self, name, mail, pwd):

        sn = model_DB.session()

        try:
            sn.add( model_DB.User(username = name, passwd = pwd, mail = mail))
            flag = True
        except:
            flag = False

        sn.commit()
        sn.close()
        return flag

    def check_user(self, name, pwd, status):
        flag = False
        sn = model_DB.session()
        if status == 1:
            u = sn.query(model_DB.User).filter(model_DB.User.username == name, or_(pwd == 'check_repeat', model_DB.User.passwd == pwd))
            if u.first():
                flag = True
        else:
            u = sn.query(model_DB.User).filter(model_DB.User.mail == name, model_DB.User.passwd == pwd)
            if u.first():
                flag = True

        print(u.first(), name, pwd, 'check_user')
        sn.close();
        return flag

class CodeHandle(BaseHandleController.BaseRequestHandleController):
    def get(self, *args, **kwargs):
        print('test.html')
        self.render('log_reg_hov.html')