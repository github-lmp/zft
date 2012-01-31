#!/usr/bin/env python
#-*- coding:utf-8 -*-

import csv
import hashlib
import os.path
import os
import sqlite3
import time

from zdashboard.common import config

def swauth_add_user(account, user, key):
    pass

def get_db_conn(user):
    path = get_db_path(user)
    conn=sqlite3.connect(path)
    conn.text_factory = str
    return conn 

def get_db_path(user):
    '''通过用户名返回一个对应的数据库路径'''
    md5 = hashlib.md5()
    md5.update(user)
    prefix = config.db_prefix
    tag = md5.hexdigest()
    return os.path.join(prefix, tag[-1:], tag[-2:], tag+'.db')

def create_nodetree_db(path, overwrite=False):
    '''
        创建一个用户的node表
    '''
    if os.path.exists(path):
        if not overwrite:
            raise Exception('%s was existed, and overwrite=False'%(path))
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as (errno, errmsg):
        pass
    with open(path, 'w') as f:
        f.write("")
    conn=sqlite3.connect(path)
    conn.text_factory = str
    c=conn.cursor()
    c.execute("""
    CREATE TABLE `nodetree` (
    		`id` INTEGER PRIMARY KEY NOT NULL,
        `name` VARCHAR(75) NOT NULL,
        `fId` INTEGER NOT NULL,
        `type` INTEGER NOT NULL,
    		`atime` TIMESTAMP DEFAULT (datetime('now', 'localtime')) NOT NULL,
        `attr` VARCHAR(75)
         );
    """)
    #fnodeId 为-1的时候，表明是最高级的节点，没有父节点。
    #除了-1之后，所有的节点Id指的是group类型的Id.
    conn.commit()
    c.close


def get_children(nodeId, nodeType, conn, tableName='nodetree'):
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

def fetch_node(node_id, conn, tableName='nodetree'):
    c=conn.cursor()
    txt=c.execute("select * from '%s' where id='%s'"
            %(tableName, node_id))
    node = ''
    for row in txt:
        node = {"id":int(row[0]), "name":row[1], 'fid':int(row[2]), 
            "type":int(row[3]), 'atime':row[4], 'attr':row[5]}
    c.close
    return node


def get_json(fnode, conn, tableName='nodetree'):
    """在构建每个节点的id时候，是其父节点和节点的id的组合，
        为了方便上层的删除操作。
        nodeId为整数，nodeType 为0(group), 1(user).
    """
    c=conn.cursor()
    print fnode,'ss'
    if fnode['type'] == 1:
        return None
    elif fnode['type'] == 0:
        json_s = {
              "data":fnode['name'], 
              "attr":{"id":"node_"+str(fnode['id'])+"_"+
                  str(fnode['fid'])+"_"+str(fnode['type']), 
              "rel":str(fnode['type'])}, 
              "children":[],
              "state":"open"} 
        children = get_children(fnode['id'], fnode['type'], conn)
        for node in children:
            json_tmp = {
                    "data":node['name'], 
                    "attr":{"id": "node_"+str(node['id'])+"_"+
                        str(fnode['id'])+"_"+str(node['type']), 
                    "rel":str(fnode['type'])},
                    "state":"open"}
            if node['type'] == 0:
                json_tmp['children'] = []
            json_s["children"].append(json_tmp)
        return json_s
    else:
        raise Exception('i do not understander your type:%s'%(nodeType))


if __name__ == "__main__":

    db = "/home/zjf/swfit_demo_db/9/b9/f5d1278e8109edd94e1e4197e04873b9.db"
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
    print 'for test'
    create_jstree_db('/home/zjf/Desktop/tmp.db', overwrite=True)
    print get_db_path('tester1')
