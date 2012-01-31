#!/usr/bin/env python
#-*- coding:utf-8 -*-

####################
## zhangjunfeng@meidisen.com
####################

import web
import os
import sys
from subprocess import Popen,PIPE
import sqlite3
import json
import time
import random


import jstree_json
DEBUG = True
db = "./static/demo_db/demo.db"
#web.config.debug=False

urls=(
    '/','Index',# #访问方式/static/html/jstree_demo.html
    '/test','Test',
    '/demo','Demo',
    )

app = web.application(urls,globals())
render = web.template.render('templates')
class Index:
    def GET(self):
        """demo.html 是相对完整的演示，index.html很简单展示"""
     #   web.seeother("static/html/index.html")
        web.seeother("static/html/jstree_demo.html")

class Demo:
    def GET(self):
        x = web.input()
        print x
        demo = x["demo"]
        if x["operation"] == "get_children":
            nodeId = x["id"].split("_")[1]
            print nodeId
            #暂时是一次行加载。下一步实现根据请求的id来实现动态加载。
            if str(nodeId) != str(-1):
                group1 = {}
            else:
                group1 = jstree_json.getJson(-1, "group")
            return json.dumps(group1)
        elif x["operation"] == "search":
            search_str = x["search_str"]
            print search_str
            group1 = jstree_json.getJson(-1, "group")
            return json.dumps(group1)
    def POST(self):
        x = web.input()
        print "in post.", x
        conn=sqlite3.connect(db)
        conn.text_factory=str
        c=conn.cursor()

        if "operation" in x.keys() and x.operation == "create_node":
            assert len(x["id"].split("_")) == 3
            nodeType = x["type"]
            nodeName = x["title"]
            fnodeId = x["id"].split("_")[1]
            if nodeType == "user":
                print "in create user."
                password = x["password"]
                (num, ) = c.execute("select count(*) from user where name = '%s'"\
                        %(nodeName))
                if num[0] == 1:
                    response = {"status": False, "id":"", "msg":"this name was existed."}
                else:
                    (num, ) = c.execute("select max(id) from user ")
                    maxId = num[0]
                    c.execute("insert into user values (null, '%s', '%s', '%s', '%s')"\
                            %(nodeName, password, fnodeId, time.ctime()))
                    response = {"status": True, \
                            "id":"node_" + fnodeId + "_" + str(maxId + 1) + "_user", "msg":"create user success."}
            elif nodeType == "group":
                print "in create group."
                permis = x["permis"]
                (num, ) = c.execute("select count(*) from grop where name = '%s'"\
                        %(nodeName))
                if num[0] == 1:
                    response = {"status": False, "id":"", "msg":"this name was existed."}
                else:
                    (num, ) = c.execute("select max(id) from grop ")
                    maxId = num[0]
                    c.execute("insert into grop values (null, '%s', '%s', '%s', '%s')"\
                            %(nodeName, fnodeId, permis, time.ctime()))
                    response = {"status": True, \
                            "id":"node_" + fnodeId + "_" + str(maxId + 1) + "_group", "msg":"create group success."}
            else:
                response = {"status": False, "id":"", "msg":"i don't know this type."}
            print nodeType, nodeName, fnodeId
        elif "operation" in x.keys() and x.operation == "remove_node":
            """         """
            #现在只支持的是cut操作。和copy操作不同点在于,x=web.input里面copy的值不同。
            #cut 操作，copy=0, copy操作,copy=1.
            assert len(x["id"].split("_")) == 3
            nodeId = x["id"].split("_")[1]
            fnodeId = x["id"].split("_")[0]
            nodeType = x["id"].split("_")[2]
            assert nodeType == "user" or nodeType == "group"
            if nodeType == "user":
                try:
                    c.execute("delete from user where id = '%s'"%(nodeId));
                    response = {"status": True, "id":"", "msg":"rename success."}
                except Exception, e:
                    response = {"status": False, "id":"", "msg":e}
            if nodeType == "group":
                try:
                    c.execute("delete from grop where id = '%s'"%(nodeId));
                    response = {"status": True, "id":"", "msg":"remove success."}
                except Exception, e:
                    response = {"status": False, "id":"", "msg":e}
            print nodeId, fnodeId
        elif "operation" in x.keys() and x.operation == "rename_node":
            assert len(x["id"].split("_")) == 3
            nodeId = x["id"].split("_")[1]
            nodeType = x["id"].split("_")[2] 
            newNodeName = x["title"]
            assert nodeType == "user" or nodeType == "group"
            if nodeType == "user":
                try:
                    c.execute("update user set name = '%s' where id = '%s'"%(newNodeName, nodeId));
                    response = {"status": True, "id":"", "msg":"rename success."}
                except Exception, e:
                    response = {"status": False, "id":"", "msg":str(e)}
            if nodeType == "group":
                try:
                    c.execute("update grop set name = '%s' where id = '%s'"%(newNodeName, nodeId));
                    response = {"status": True, "id":"", "msg":"rename success."}
                except Exception, e:
                    response = {"status": False, "id":"", "msg":str(e)}

        elif "operation" in x.keys() and x.operation == "move_node":
            copy = x["copy"]
            nodeId = x["id"].split("_")[1]
            nodeType = x["id"].split("_")[2]
            oldFnode = x["id"].split("_")[0]
            newFnodeId = x["ref"].split("_")[1] 
            assert nodeType == "user" or nodeType == "group"
            if nodeType == "user":
                try:
                    c.execute("update user set grop = '%s' where id = '%s'"%(newFnodeId, nodeId));
                    response = {"status": True, "id":"", "msg":"move success."}
                except Exception, e:
                    response = {"status": False, "id":"", "msg":str(e)}
            if nodeType == "group":
                try:
                    c.execute("update grop set grop = '%s' where id = '%s'"%(newFnodeId, nodeId));
                    response = {"status": True, "id":"", "msg":"move success."}
                except Exception, e:
                    response = {"status": False, "id":"", "msg":str(e)}
        else:
            c.close()
            return web.internalerror(message = "now don't support this operation!")

        conn.commit()
        c.close()
        print response
        return json.dumps(response) 

#       return web.internalerror(message = "hello,for test!")


class Test:
    def GET(self):
        x = web.input()
        print x
        demo = x["demo"]
        if demo == "demo01" or demo == "demo04":
#          data = open("./static/js/_docs/_json_data.json", "r").readlines()
#            data =[ { "data" : "A node", "children" : [ { "data" : "Only child", "state" : "closed" ,"attr":{"id":"node_child_1"}} ], "state" : "open", "attr":{"id":"node_A"}}]
#            d =[ { "data" : "B node", "children" : [ { "data" : "Only child", "state" : "closed" ,"attr":{"id":"node_child_d"}} ], "state" : "open", "attr":{"id":"node_B"}}]
#            data.append(d)
            group1 = [{\
                "data": "group1", \
                "children":[{"data":"group1_user1", "state":"open",\
                                        "children":[\
                                            {"data":"group1_user1_user1", "state":"close", "attr":{"id":"node_group1_user1_user1"}}\
                                                    ],\
                               "attr":{"id":"node_group1_user1"}},\
                            {"data":"group1_user2", "state":"close", "attr":{"id":"node_group1_user2"}},\
                    ],\
                "attr":{"id":"node_group1"},\
                }]
            group2 = [{\
                "data": "group2", \
                "children":[{"data":"group2_user1", "state":"open", "attr":{"id":"node_group2_user1"}},\
                            {"data":"group2_user2", "state":"close", "attr":{"id":"node_group2_user2"}},\
                    ],\
                "attr":{"id":"node_group2"},\
                }]

            group1.append(group2) 
            if x["id"] == str(1):
                print x["id"]
                return json.dumps(group1) 
            else:
                return json.dumps("")

    def POST(self):
        x = web.input()
        print "in post.", x
        return "success"
#        return web.internalerror(message = "hello,for test!")

if __name__=="__main__":
    app.run()


#            group1 = [{\
#                "data": "group1", \
#                "children":[{"data":"group1_group1", "state":"open",\
#                                        "children":[\
#                                        {"data":"group1_group1_user1", "state":"close", "attr":{"id":"node_group1_group1_user1", "rel":"user"}}\
#                                                    ],\
#                                                    "attr":{"id":"node_group1_user1", "rel":"group"}},\
#                               {"data":"group1_user2", "state":"close", "attr":{"id":"node_group1_user2", "rel":"user"}},\
#                    ],\
#                    "attr":{"id":"node_group1", "rel":"group"},\
#                }]
#            group2 = [{\
#                "data": "group2", \
#                "children":[{"data":"group2_user1", "state":"open", "attr":{"id":"node_group2_user1"}, "children":[]},\
#                {"data":"group2_user2", "state":"close", "attr":{"id":"node_group2_user2"}, "children":[]},\
#                    ],\
#                "attr":{"id":"node_group2"},\
#                }]
#            group1.append(group2) 
