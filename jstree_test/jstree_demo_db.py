#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sqlite3
import os.path
import os
import time
import csv



#################################################
#初始化数据库
db="/home/zjf/demo_db/demo.db"
DEBUG = True #True/False
input=""
if os.path.exists(db):
    while True:
        input=raw_input("""
             %s is existed,
             do you want to del it ? 
             continue input yes,exit input no. yes/no:"""%(db))
        sinput=input.strip()
        if sinput == "yes" or sinput == "no":
            break
        print "please input yes or no ."
    if sinput == "yes":
        newName = time.time()
        os.rename(db,db + "_time_" + str( newName) + "_bak" )
        os.remove(db)
    if sinput == "no":
        print "you exit."
        exit()
else:
    dir=os.path.dirname(db)
    try:
        os.makedirs(dir)
    except OSError as (errno, errmsg):
        print errmsg
    f=open(db,"w")
    f.write("")
    f.close()
####################################################


####################################################
#id, nodeName, nodeId, fnodeId, nodeType
#jstree_test table
conn=sqlite3.connect(db)
conn.text_factory=str
c=conn.cursor()
c.execute("""
CREATE TABLE `jstree` (
		  `id` INTEGER PRIMARY KEY NOT NULL,
      `nodeName` VARCHAR(75) NOT NULL,
      `fnodeId` INTEGER NOT NULL,
      `nodeType` VARCHAR(75) NOT NULL,
		  `atime` TIMESTAMP DEFAULT  (datetime('now', 'localtime')) NOT NULL,
      `nodeNote` VARCHAR(75),
       );
""")
#fnodeId 为-1的时候，表明是最高级的节点，没有父节点。除了-1之后，所有的节点Id指的是group类型的Id.
conn.commit()

if DEBUG:
    # id ,nodeName, nodeId, fnodeId, nodeType,
    c.execute("""INSERT INTO jstree  VALUES  ( 'G1',  'g1', -1, 'group') ;""")
    c.execute("""INSERT INTO jstree  VALUES  ( 'G2', 'g2', -1, 'group') ;""")
    c.execute("""INSERT INTO jstree  VALUES  ( 'G3', 'g3', '-1', 'group') ;""")
    c.execute("""INSERT INTO jstree  VALUES  ( 'G11', 'g4', 'g1', 'group') ;""")
    c.execute("""INSERT INTO jstree  VALUES  ( 'G12', 'g5' , 'g1', 'group') ;""")
    c.execute("""INSERT INTO jstree  VALUES  ( 'G13', 'g6', 'g1', 'group') ;""")

    c.execute("""INSERT INTO jstree  VALUES ( 'u11', 'u1', 'g1', 'user')""")
    c.execute("""INSERT INTO jstree  VALUES ( 'u111', 'u2', 'g4', 'user' )""")
    c.execute("""INSERT INTO jstree  VALUES ( 'u112', 'u3', 'g4', 'user' )""")
    c.execute("""INSERT INTO jstree  VALUES ( 'u113', 'u4', 'g4', 'user' )""")
    c.execute("""INSERT INTO jstree  VALUES ( 'u121', 'u5', 'g5', 'user' )""")
    c.execute("""INSERT INTO jstree  VALUES ( 'u122', 'u6', 'g5', 'user' )""")
    c.execute("""INSERT INTO jstree  VALUES ( 'u131', 'u7', 'g6', 'user' )""")
    conn.commit()
    txt=c.execute("""select * from jstree """)
    for row in txt:
        for el in row:
            print unicode(str(el),"utf-8"),
        print 
c.close
