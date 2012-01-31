#!/usr/bin/env python
#! -*- coding:utf-8 -*-
import os


DEBUG = True #运行的时候，可以设置为False


#swift 的相关信息
#根据实际情况修改下面的值
swiftHost="192.168.56.186:8080"

#在本程序中假定swift用的auth是swauth
#按照SAIO的创建用户方式创建用户
#swauth-add-user -K swauthkey -a swift swifter swifting

#用来存放数据库
#/home/zjf/swfit_demo_db/9/b9/f5d1278e8109edd94e1e4197e04873b9.db
db_prefix = '/home/zjf/swfit_demo_db/'
