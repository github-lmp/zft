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

from common import config


web.config.debug = config.DEBUG


urls=(
    '/','Index',
    '/node/(.+)','Node',
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
        pass
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

class Node:
    '''/node/0|1/(id) 添加一个属性是 '''
    def GET(self, path):
        '''获取目录下的内容,或下载某个文件'''
        return 'get', path
    def POST(self):
        return 'post'
    def PUT(self):
        '''创建一个目录，或上创一个文件 '''
        return 'put'
    def DELETE(self):
        return 'delete'
    def COPY(self):
        return 'copy'
    def MOVE(self):
        return 'move'

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
        web.ctx.session.account = account
        web.ctx.session.username = username
        raise web.seeother("/")


class Index:
    @login
    def GET(self):
        x = web.input()
        return render.index2(respl, contentl)

if __name__=="__main__":
    app.add_processor(web.loadhook(session_hook))
    app.run()
