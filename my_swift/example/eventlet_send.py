#!/usr/bin/evn python
#!coding:utf-8

import eventlet
from eventlet.green import socket, httplib
#import httplib
import time

chunk_size = 65535
def geturl(url):
    c = socket.socket()
    ip = socket.gethostbyname(url)
    print ip
    ip = '0.0.0.0'
    c.connect((ip, 8080))
    print '%s connected' % url
    c.sendall('GET /\r\n\r\n')
    return c.recv(1024)


def put():
    put_send_name = '/data/iso/ubuntu-10.04-server-amd64.iso'
    put_save_name = '/data/iso/server_save_name'
    length = 0
    lines = []
    with open(put_send_name, 'rb') as f:
        for i in f:
            pass
        length = f.tell()
    conn = httplib.HTTPConnection('127.0.0.1:8080')
    conn.putrequest('PUT',  '/index.html')
    #conn.putheader('Content-Length', length)
    conn.putheader('Transfer-Encoding', 'chunked')
    conn.putheader('x-file-name', put_save_name)
    conn.endheaders()
    with open(put_send_name, 'rb') as f:
        n = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                conn.send("0\r\n\r\n")
                break
            conn.send('%x\r\n%s\r\n'%(len(chunk), chunk))
            n += 1
    r1 = conn.getresponse()
    print r1.status, r1.reason, n


def get():
    get_recv_name = '/data/iso/server_save_name'
    get_save_name = '/data/iso/ubuntu-10.04-server-amd64.iso_my_get'
    conn = httplib.HTTPConnection('127.0.0.1:8080')
    conn.request('GET', '', headers={'x-file-name':get_recv_name})
    r1 = conn.getresponse()
    with open(get_save_name, 'wb') as f:
        while True:
            chunk = r1.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
    #print r1.status, r1.reason, r1.read(), r1.length

if __name__ == '__main__':
    print '你好'
    put()
    #print '*'*100
    #get()
