#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sqlite3
import os.path
import os
import time
import csv



db="/home/zjf/swfit_demo_db/9/b9/f5d1278e8109edd94e1e4197e04873b9.db"

####################################################
#id, nodeName, nodeId, fnodeId, nodeType
#jstree_test table
conn=sqlite3.connect(db)
conn.text_factory=str
c=conn.cursor()
#fnodeId 为-1的时候，表明是最高级的节点，没有父节点。除了-1之后，所有的节点Id指的是group类型的Id.
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


# id ,nodeName, nodeId, fnodeId, nodeType,
c.execute("""INSERT INTO nodetree  VALUES  (0, 'G1', -1, 0, '', '');""")
c.execute("""INSERT INTO nodetree  VALUES  (1, 'G2', -1, 0, '', '');""")
c.execute("""INSERT INTO nodetree  VALUES  (2, 'G3', -1, 0, '', '');""")
c.execute("""INSERT INTO nodetree  VALUES  (3, 'G11', 1, 0, '', '');""")
c.execute("""INSERT INTO nodetree  VALUES  (4, 'G12', 2, 0, '', '');""")
c.execute("""INSERT INTO nodetree  VALUES  (5, 'G13', 3, 0, '', '');""")

c.execute("""INSERT INTO nodetree  VALUES (6, 'u11', 1, 1, '', '')""")
c.execute("""INSERT INTO nodetree  VALUES (7, 'u111', 2, 1, '', '')""")
c.execute("""INSERT INTO nodetree  VALUES (8, 'u112', 3, 1, '', '')""")
c.execute("""INSERT INTO nodetree  VALUES (9, 'u113', 4, 1, '', '')""")
c.execute("""INSERT INTO nodetree  VALUES (10, 'u121', 5, 1, '', '')""")
c.execute("""INSERT INTO nodetree  VALUES (11, 'u122', 6, 1, '', '')""")
c.execute("""INSERT INTO nodetree  VALUES (12, 'u131', 7, 1, '', '')""")
conn.commit()
txt=c.execute("""select * from nodetree """)
for row in txt:
    for el in row:
        print unicode(str(el),"utf-8"),
    print 
c.close
