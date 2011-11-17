#!/usr/bin/env python
#coding:utf-8 
from webob import Request, Response

class Auth(object):
    def __init__(self, app, allowed_username):
        self.app = app
        self.allowed_usernames = allowed_username
 
    def __call__(self, env, start_response):
        #if env.get('REMOTE_USER') not in self.allowed_usernames:
        if True:
            return self.app(env, start_response)
        status = '403 Forbidden'
        response_header = [('Content-type', 'text/plain')] 
        start_response(status, response_header)
        return ['You are forbidden to view this resource!\n']
        pass
 
def filter_factory(global_conf, **local_conf):
    """Returns a WSGI filter app for use with paste.deploy."""
    conf = global_conf.copy()
    conf.update(local_conf)

    allowed_username = ['a', 'b']
    def auth_filter(app):
        return Auth(app, allowed_username)
    return auth_filter  

if __name__ == "__main__":
    print '你好'
