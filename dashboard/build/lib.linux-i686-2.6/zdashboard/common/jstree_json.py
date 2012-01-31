#!/usr/bin/env python #-*- coding:utf-8 -*- import os
import random
import sys
from subprocess import Popen,PIPE
import sqlite3
import json
import time
import web

DEBUG = True
db = "/home/zjf/swfit_demo_db/9/b9/f5d1278e8109edd94e1e4197e04873b9.db"
tableName = "nodetree"

    #c.execute("""
    #CREATE TABLE `nodetree` (
        #`id` INTEGER PRIMARY KEY NOT NULL,
        #`name` VARCHAR(75) NOT NULL,
        #`fId` INTEGER NOT NULL,
        #`type` INTEGER NOT NULL,
        #`atime` TIMESTAMP DEFAULT (datetime('now', 'localtime')) NOT NULL,
        #`attr` VARCHAR(75)
         #);
    #""")
conn=sqlite3.connect(db)
conn.text_factory=str


def get_children(nodeId, nodeType, conn):
    """接受一个nodeId, 和该节点的类型。 返回它的子节点的Id和类型。 """
    if nodeType == 1:
        return []
    elif nodeType == 0:
        c=conn.cursor()
        txt=c.execute("select * from '%s' where fId='%s'"
                %(tableName, nodeId))
        child = []
        for row in txt:
            print "row:%s"%str(row), row[0]
            child.append({"id":row[0], "name":row[1], 'fid':row[2], 
                "type":row[3], 'atime':row[4], 'attr':row[5]})
        c.close
        return child
    else:
        raise Exception('i do not understander your type:%s'%(nodeType))

def get_json(fnode, conn):
    """在构建每个节点的id时候，是其父节点和节点的id的组合，
        为了方便上层的删除操作。
        nodeId为整数，nodeType 为0(group), 1(user).
    """
    c=conn.cursor()
    if fnode['type'] == 1:
        return None
    elif fnode['type'] == 0:
        json_s = {
              "data":fnode['id'], 
              "attr":{"id":"node_"+str(fnode['id'])+"_"+
                  str(fnode['fid'])+"_"+str(fnode['type']), 
              "rel":fnode['type']}, 
              "children":[],
              "state":"open"} 
        children = get_children(fnode['id'], fnode['type'], conn)
        if children == []:
            return json_s
        else:
            for node in children:
                json_tmp = {
                        "data":node['id'], 
                        "attr":{"id": "node_"+str(node['id'])+"_"+
                            str(fnode['id'])+"_"+str(fnode['type']), 
                        "rel":fnode['type']},}
                json_s["children"].append(json_tmp)
            return json_s
    else:
        raise Exception('i do not understander your type:%s'%(nodeType))



if __name__=="__main__":
    nodes  = get_children(-1, 0, conn)
    for node in nodes:
        print get_json(node, conn)
