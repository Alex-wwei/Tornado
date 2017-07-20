import tornado.web

class BaseRequestHandleController(tornado.web.RequestHandler):
    def initialize(self):
        self.session = None