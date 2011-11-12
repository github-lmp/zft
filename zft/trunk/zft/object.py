#!/usr/bin/env python
#coding:utf-8

'''object server '''

import os
import functools
import tracback

from wsgiref.simple_server import make_server
from webob.exc import HTTPAccepted, HTTPBadRequest, HTTPCreated, \
     HTTPInternalServerError, HTTPNoContent, HTTPNotFound, \
     HTTPNotModified, HTTPPreconditionFailed, \
     HTTPRequestTimeout, HTTPUnprocessableEntity, HTTPMethodNotAllowed
from webob import Request, Response
from paste.deploy import loadapp
from zft.utils import check_utf8


def public(func):
    """
    Decorator to declare which methods are public accessible as HTTP requests
    :param func: function to make public
    """
    func.publicly_accessible = True
    @functools.wraps(func)
    def wrapped(*a, **kw):
        return func(*a, **kw)
    return wrapped


class DiskFile(object):
    def __init__(self):
        pass

class ObjectController(object):
    def __init__(self, path):
        self.path = path 
        pass

    def GET(self, req):
        return 'get'

    def HEAD(self, req):
        return 'head'

    def POST(self, req):
        return 'post'

    def PUT(self, req):
        etag = 'etag'
        resp = HTTPCreated(request=req, etag=etag)
        return resp

    def DELETE(self, req):
        return 'delete'

    def COPY(self, req):
        return 'copy'

    def __call__(self, env, start_response):
        """WSGI Application entry point for the Swift Object Server."""
        start_time = time.time()
        req = Request(env)
        if not check_utf8(req.path_info):
            res = HTTPPreconditionFailed(body='Invalid UTF8')
        else:
            try:
                if hasattr(self, req.method):
                    res = getattr(self, req.method)(req)
                else:
                    res = HTTPMethodNotAllowed()
            except:
                res = HTTPInternalServerError(body=traceback.format_exc())
        trans_time = time.time() - start_time
        if req.method in ('PUT', 'DELETE'):
            slow = self.slow - trans_time
            if slow > 0:
                sleep(slow)
        return res(env, start_response)

def app_factory(global_conf, **local_conf):
    conf = global_conf.copy()
    conf.update(local_conf)
    return ObjectController(conf)

if __name__ == "__main__":
    port = 9000
    conf_path = os.path.join(os.getcwd(), 'config.ini')
    app = loadapp('config:%s'%(conf_path), global_conf={'global_conf': 'global_conf'})
    httpd = make_server('', port, app)
    print 'Server HTTP on port %s...'%(port)
    httpd.serve_forever()
    httpd.handle_request()
