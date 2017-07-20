import tornado.web, tornado.ioloop, re

class BaseField(object):
    def __init__(self, error_dict, required = True, ):
        self.error_dict = {}
        if error_dict:
            self.error_dict.update(error_dict)
        self.error = None
        self.required = required
        self.is_valid = False
        self.vlaue = None
    def validate(self, name, input_value):
        if not self.required:
            self.is_valid = True
        else:
            if name != 'check_box':
                input_value = input_value.strip()
            if len(input_value) == 0:
                self.error = name + self.error_dict['required']
            else:
                if name == 'check_box':
                    self.is_valid = True
                else:
                    if re.match(self.REGULAR, input_value):
                        self.is_valid = True
                    else:
                        self.error = name + self.error_dict['valid']
        return self.is_valid, self.error
class IPField(BaseField):
    REGULAR = "^(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|[1-9])\\."+"(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\."+"(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\."+"(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)$"

class PHONEField(BaseField):
    REGULAR = '^1[3|4|5|8]\d{9}$'

class MAILField(BaseField):
    REGULAR = "^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"

class CHECK_BOX_Field(BaseField):
    REGULAR = None
class Base_check(object):
    def check_values(self, handle):
        flag = True
        content = {}
        for key, regular in self.__dict__.items():
            if key == 'check_box':
                value =  handle.get_arguments(key)
            else:
                value = handle.get_argument(key)
            info, error = regular.validate(key, value)
            if info:
                content[key] = value
            else:
                content[key] = error
                flag = info
        return flag, content

class Check_value(Base_check):
    def __init__(self):
        self.IP = IPField(required=True, error_dict={'required':'不能为空哦！','valid':'输入格式错误！'})
        self.PHONE = PHONEField(required=True, error_dict={'required':'不能为空哦！','valid':'输入格式错误！'})
        self.MAIL = MAILField(required=True, error_dict={'required':'不能为空哦！','valid':'输入格式错误！'})
        self.check_box = CHECK_BOX_Field(required=True, error_dict={'required':'不能为空哦！','valid':'输入格式错误！'})

class Indexhandle(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
    def post(self, *args, **kwargs):
        check = Check_value()

        flag, content = check.check_values(self)
        print(content)
        if flag:
            self.write('success')
        else:
            self.write('fault')


settings = {
    'template_path':'views',
    'static_path':'statics',

}

if __name__ == '__main__':
    app = tornado.web.Application([
        (r'/index', Indexhandle),

    ], **settings)

    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()