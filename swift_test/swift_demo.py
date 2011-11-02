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
    '/login','Login',
    '/logout', 'Logout',
    '/ccont','Ccont',
    '/dcont','Dcont',
    '/upload_object','Upload_object',
    '/delete_object','Delete_object',
    '/retrieve_object','Retrieve_object',
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


def login(func):
    """登录返回执行func,，否则返回login页面"""
    def newFunc(*args, **kwargs):
        session = web.ctx.session
        if session.logged==1:
            return func(*args, **kwargs)
        else:
            return render.login()
    return newFunc

class Logout:
    def GET(self):
        web.ctx.session.kill()
        raise web.seeother('/')

class Login:
    def GET(self):
        x = web.input()
    def POST(self):
        x = web.input()
        account = x["account"]
        username = x["username"]
        password = x["password"]

        h = httplib2.Http(".cache")
        respl = []
        contentl = []
        XStorageUser = account + ":" + username
        XStoragePass = password
        resp, content = h.request("http://" + config.swiftHost + \
                "/auth/v1.0", "GET", headers={"X-Storage-User":\
                 XStorageUser, "X-Storage-Pass":XStoragePass})
        print resp, resp.status, content
        if resp.status == 200:
            web.ctx.session.logged = 1
        else:
            return "login error."
        web.ctx.session.XAuthToken = resp["x-auth-token"]
        web.ctx.session.XStorageUrl = resp["x-storage-url"].replace(
                    '127.0.0.1:8080',  config.swiftHost)
        raise web.seeother("/")


class Index:
    @login
    def GET(self):
        x = web.input()
        h = httplib2.Http(".cache")
        respl = []
        contentl = []
        print '----------', web.ctx.session.XStorageUrl, web.ctx.session.XAuthToken
        resp, content =  h.request(
                web.ctx.session.XStorageUrl, "GET", \
                headers={"X-Auth-Token":web.ctx.session.XAuthToken})
        container = content.split("\n")[:-1]
        print 'resp:', resp, content
        respl.append(resp)
        contentl.append(container)
        for i in range(int(resp['x-account-container-count'])):
            print i, container[i]
            resp, content = h.request(web.ctx.session.XStorageUrl + "/" + \
                    container[i], "GET", \
                headers={"X-Auth-Token":web.ctx.session.XAuthToken})
            print resp, content
            respl.append(resp)
            contentl.append(container[i] + ":" + \
                    str(content.split("\n")[:-1]))
        return render.index(respl, contentl)


class Ccont:
    """ ccont = create container    """
    def POST(self):
        x = web.input()
        print x
        ccont_name = x["ccont_name"]
        h = httplib2.Http(".cache")
        print 'web.ctx.session', web.ctx.session
        resp, content = h.request(web.ctx.session.XStorageUrl + "/" + \
                ccont_name, "PUT", \
                headers={"X-Auth-Token":web.ctx.session.XAuthToken})
        print resp, content
        return render.index(resp, content)


class Dcont:
    """ ccont = create container    """
    def POST(self):
        x = web.input()
        print x
        ccont_name = x["ccont_name"]
        h = httplib2.Http(".cache")
        resp, content = h.request(web.ctx.session.XStorageUrl + "/" + \
                ccont_name, "DELETE", \
                headers={"X-Auth-Token":web.ctx.session.XAuthToken})
        print resp, content
        return render.index(resp, content)


class Upload_object:
    """    """
    def POST(self):
        x = web.input()
        data = x["file"]
        ccont_name = x["ccont_name"]
        filename = x["filename"]
        h = httplib2.Http(".cache")
        resp, content = h.request(web.ctx.session.XStorageUrl + "/" + \
                ccont_name + "/" + filename, "PUT", data,\
                headers={"X-Auth-Token":web.ctx.session.XAuthToken})
        print resp, content
        return render.index(resp, content)

class Delete_object:
    """    """
    def POST(self):
        x = web.input()
        ccont_name = x["ccont_name"]
        filename = x["filename"]
        h = httplib2.Http(".cache")
        resp, content = h.request(web.ctx.session.XStorageUrl + \
                "/" + ccont_name + \
                "/" + filename, "DELETE", \
                headers={"X-Auth-Token":web.ctx.session.XAuthToken})
        print resp, content
        return render.index(resp, content)

class Retrieve_object:
    """    """
    def POST(self):
        x = web.input()
        ccont_name = x["ccont_name"]
        filename = x["filename"]
        h = httplib2.Http(".cache")
        resp, content = h.request(web.ctx.session.XStorageUrl + "/" + \
                ccont_name + "/" + filename, "GET", \
                headers={"X-Auth-Token":web.ctx.session.XAuthToken})
        return content
#        return render.index(resp, content)


if __name__=="__main__":
    app.add_processor(web.loadhook(session_hook))
    app.run()
