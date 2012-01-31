#!/usr/bin/env python
#-*- coding:utf-8 -*-

import csv
import hashlib
import os.path
import os
import sqlite3
import time

import config

def swauth_add_user(account, user, key):
    pass

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
    conn.text_factory=str
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

if __name__ == "__main__":
    print 'for test'
    create_jstree_db('/home/zjf/Desktop/tmp.db', overwrite=True)
    print get_db_path('tester1')
