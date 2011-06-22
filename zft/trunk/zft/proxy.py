#!/usr/bin/env python
#coding:utf-8 
import os

from wsgiref.simple_server import make_server
from webob.exc import HTTPNotFound, HTTPMethodNotAllowed
from webob import Request, Response
from paste.deploy import loadapp

class ObjectController(object):
    def __init__(self, dev):
        self.dev = dev
        pass

    def GET(self, req):
        return 'get'

    def HEAD(self, req):
        return 'head'

    def POST(self, req):
        return 'post'

    def PUT(self, req):
        return 'put'

    def DELETE(self, req):
        return 'delete'

    def COPY(self, req):
        return 'copy'

class Application(object):
    def __init__(self, conf):
        '''req.path 文件名 '''
        pass

    def __call__(self, env, start_response):
        print env
        try:
            req = self.update_request(Request(env))
            response = self.handle_request(req)(env, start_response)
            return response
        except Exception:
            status = '500 server error'
            response_header = [('Content-type', 'text/plain')] 
            start_response(status, response_header)
            return ['Internal server error, application!\n']
    
    def update_request(self, req):
        return req

    def handle_request(self, req):
        try:
            controller, path = self.get_controller(req.path)
        except ValueError:
            return HTTPNotFound(request=req)
        controller = controller(path)
        try:
            hander = getattr(controller, req.method)
        except AttributeError:
            hander = None
        if not hander:
            return HTTPMethodNotAllowed(request=req)
        return hander(req)

    def get_controller(self, path):
        return ObjectController, path

def app_factory(global_conf, **local_conf):
    conf = global_conf.copy()
    conf.update(local_conf)
    return Application(conf)

if __name__ == "__main__":
    conf_path = os.path.join(os.getcwd(), 'config.ini')
    app = loadapp('config:%s'%(conf_path), global_conf={'global_conf': 'global_conf'})
    httpd = make_server('', 8000, app)
    print 'Server HTTP on port 8000...'
    httpd.serve_forever()
    httpd.handle_request()
    print '你好'
