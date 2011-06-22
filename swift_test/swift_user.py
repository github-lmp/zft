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
from web.contrib.template import render_jinja

# 下面的import 是从common目录里面导入的。
sys.path.append( os.path.join(os.getcwd(), "common") )
import config


#web.config.debug=False


urls=(
    '/user','User',
        )

app = web.application(urls,globals())
render = render_jinja('templates', encoding = "utf8")
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

class Login:
    def GET(self):
        x = web.input()
        if "do" in x.keys() and x["do"] == "logout":
            session.kill()
            web.seeother("/")
    def POST(self):

#        x = web.input()
#        print "login error.", x
#        account = x["account"]
#        username = x["username"]
#        password = x["password"]
#        if account == config.account and username == \
#                config.username and password == config.password:
#            session.logged = 1
#            h = httplib2.Http(".cache")
#            respl = []
#            contentl = []
#            XStorageUser = account + ":" + username
#            XStoragePass = password
#            print "http://" + config.swiftHost + "/auth/v1.0"
#            resp, content = h.request("http://" + config.swiftHost + \
#                    "/auth/v1.0", "GET", headers={"X-Storage-User":\
#                    XStorageUser, "X-Storage-Pass":XStoragePass})
#            print resp["x-auth-token"]
#            config.XAuthToken = resp["x-auth-token"]
#            session.XAuthToken = resp["x-auth-token"]
#            print resp, content
#            web.seeother("/")
#        else:
#            print  x["account"], x["username"], x["password"]
#            return "login error."
        pass

class User:
    def GET(self):
        user = ["user1", "user2"]
        return render.user(user = user)
    def POST(self):
        x = web.input()
        print x
        if "option" in x.keys() and x["option"] == "useradd":
            return "test, add ok."
        
      

if __name__=="__main__":
    app.run()
