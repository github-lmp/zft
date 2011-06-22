#!/usr/bin/env python
#! -*- coding:utf-8 -*-
import os


DEBUG = True #运行的时候，可以设置为False


#begin
#swift 的相关信息
#根据实际情况修改下面的值
swiftHost="192.168.1.218:8080"

#在本程序中假定swift用的auth是swauth
#swauth-add-user -K swauthkey -a swift swifter swifting
#根据swauth-add-user的结果修改下面的值
account = "swift"
username = "swifter"
password = "swifting"
XStorageUrl = "http://192.168.1.218:8080/v1/AUTH_83508553-3729-46ba-9f0c-c83c9a3ec142" 
#xauthtoken 每次会自动更新，这里值为空
XAuthToken = ""

#end
