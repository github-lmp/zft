#!/usr/bin/env python
#-*- coding:utf-8 -*-


import web
import os
import sys
from subprocess import Popen,PIPE
import sqlite3
import json
import time
import random
import json

import httplib2
from webob import Request, Response

# 下面的import 是从common目录里面导入的。
sys.path.append( os.path.join(os.getcwd(), "common") )
import config


#web.config.debug=False


urls=(
    '/','Index',
    )

app = web.application(urls,globals())
render = web.template.render('templates')
if web.config.get('_session') is None:
    session = web.session.Session(\
            app,web.session.DiskStore('sessions'),\
            initializer={'logged':0}
            )
    web.config._session=session
else:
    session = web.config._session

#让子应用可以使用session。
def session_hook():
    web.ctx.session = session
app.add_processor(web.loadhook(session_hook))


def login(func):
    """登录返回执行func,，否则返回login页面"""
    def newFunc(*args, **kwargs):
        if session.logged==1:
            return func(*args, **kwargs)
        else:
            return render.login()
    return newFunc

class Index:
    @login
    def GET(self):
        print x

if __name__=="__main__":
    app.run()
