#!/usr/bin/env python
#coding:utf-8 
import os

from wsgiref.simple_server import make_server
from paste.deploy import loadapp

class ObjectController(object):
    def __init__(self):
        pass


class Application(object):
    def __init__(self, conf):
        pass

    def __call__(self, env, start_response):
        print env
        status = '200 0k'
        response_header = [('Content-type', 'text/plain')] 
        start_response(status, response_header)
        return ['hello world!\n']
        pass

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
