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

import httplib
from webob import Request, Response

from zdashboard.common import config
from zdashboard.common import utils


#web.config.debug = config.DEBUG


urls=(
    '/','Index',
    '/node/(.+)','Node',
    '/jstree','Jstree',
    '/login','Login',
    '/logout', 'Logout',
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

class Jstree:
    def GET(self):
        x = web.input()
        print x
        if x['operation'] == 'get_children':
            node_id = x["id"].split("_")[0]
            node_type = x["id"].split("_")[-1]
            print node_id, node_type
            raise web.seeother('/node/%s/%s'%(node_type, node_id))

    def POST(self):
        x = web.input()
        print x
        if x['operation'] == 'create_node':
            node_id = x["id"].split("_")[0]
            node_fid = x["id"].split("_")[1]
            node_type = x["id"].split("_")[-1]
            name = x['name']
            tag = x['tag']


class Node:
    '''/node/0|1/(id) 添加一个属性是 '''
    def GET(self, path):
        '''获取目录下的内容,或下载某个文件'''
        x = web.input()
        node_type, node_id = map(int, path.split('/'))
        print node_type, node_id
        conn = utils.get_db_conn(web.ctx.session.username)
        if not node_type == 0:
            return 'get', path
        if node_id == -1:
            node = {"id":-1, "name":'root', 'fid':-2, 
            "type":0, 'atime':'', 'attr':''}
        else:
            node = utils.fetch_node(node_id, conn)
        json_s = utils.get_json(node, conn) 
        print json_s
        if node_id == -1: 
            return json.dumps(json_s)
        else:
            return json.dumps(json_s['children'])

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
    def HEAD(self):
        return 'head'
    

class Login:
    def GET(self):
        x = web.input()
    def POST(self):
        x = web.input()
        account = x["account"]
        username = x["username"]
        password = x["password"]
        conn = httplib.HTTPConnection(config.swiftHost)
        conn.putrequest('GET',  '/auth/v1.0')
        conn.putheader('X-Storage-User', ":".join([account, username]))
        conn.putheader('X-Storage-Pass', password)
        conn.endheaders()
        r = conn.getresponse()
        web.ctx.session.x_auth_token = r.getheader("x-auth-token")
        web.ctx.session.x_storage_url = r.getheader("x-storage-url").replace(
                    '127.0.0.1:8080',  config.swiftHost)
        web.ctx.session.account = account
        web.ctx.session.username = username
        web.ctx.session.logged = 1
        raise web.seeother("/static/html/index2.html")
        #return r.status, r.reason, r.getheaders(), r.read()

class Index:
    @login
    def GET(self):
        #return render.index2()
        raise web.seeother("/static/html/index2.html")

if __name__=="__main__":
    app.add_processor(web.loadhook(session_hook))
    app.run()
