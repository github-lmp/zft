#!/usr/bin/env python
#!coding:utf-8

import errno
import os
import signal
import sys
import time
import mimetools
from hashlib import md5

import eventlet
from eventlet import greenio, GreenPool, sleep, wsgi, listen
from paste.deploy import loadapp, appconfig

# Hook to ensure connection resets don't blow up our servers.
# Remove with next release of Eventlet that has it in the set already.
from errno import ECONNRESET
wsgi.ACCEPT_ERRNO.add(ECONNRESET)

from eventlet.green import socket, ssl

from webob import Request, Response
from webob.exc import HTTPAccepted, HTTPCreated

chunk_size = 65535
def get_socket(default_port=8080):
    """Bind socket to bind ip:port in conf

    :param conf: Configuration dict to read settings from
    :param default_port: port to use if not specified in conf

    :returns : a socket object as returned from socket.listen or
               ssl.wrap_socket if conf specifies cert_file
    """
    bind_addr = ('0.0.0.0', default_port)
    sock = None
    retry_until = time.time() + 30
    while not sock and time.time() < retry_until:
        try:
            sock = listen(bind_addr)
        except socket.error, err:
            if err.args[0] != errno.EADDRINUSE:
                raise
            sleep(0.1)
    if not sock:
        raise Exception('Could not bind to %s:%s after trying for 30 seconds' %
                        bind_addr)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # in my experience, sockets can hang around forever without keepalive
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 600)
    return sock


def run_wsgi(app, *args, **kwargs):
    """
    """
    worker_count = kwargs.get('worker_count', 1)
    #capture_stdio(logger)
    # bind to address and port
    sock = get_socket()
    # remaining tasks should not require elevated privileges
    #drop_privileges(conf.get('user', 'swift'))

    def run_server():
        wsgi.HttpProtocol.default_request_version = "HTTP/1.1"
        eventlet.hubs.use_hub('poll')
        eventlet.patcher.monkey_patch(all=False, socket=True)
        pool = GreenPool(size=1024)
        try:
            wsgi.server(sock, app)
        except socket.error, err:
            if err[0] != errno.EINVAL:
                raise
        pool.waitall()

    # Useful for profiling [no forks].
    if worker_count == 0:
        run_server()
        return

    def kill_children(*args):
        """Kills the entire process group."""
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        running[0] = False
        os.killpg(0, signal.SIGTERM)

    def hup(*args):
        """Shuts down the server, but allows running requests to complete"""
        logger.error('SIGHUP received')
        signal.signal(signal.SIGHUP, signal.SIG_IGN)
        running[0] = False

    running = [True]
    signal.signal(signal.SIGTERM, kill_children)
    signal.signal(signal.SIGHUP, hup)
    children = []
    while running[0]:
        while len(children) < worker_count:
            pid = os.fork()
            if pid == 0:
                signal.signal(signal.SIGHUP, signal.SIG_DFL)
                signal.signal(signal.SIGTERM, signal.SIG_DFL)
                run_server()
                return
            else:
                children.append(pid)
        try:
            pid, status = os.wait()
            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                children.remove(pid)
        except OSError, err:
            if err.errno not in (errno.EINTR, errno.ECHILD):
                raise
        except KeyboardInterrupt:
            break
    greenio.shutdown_safe(sock)
    sock.close()


class Application(object):
    def __init__(self, name):
        self.name = name
        pass

    def __call__(self, env, start_response):
        #print env
        req = Request(env)
        print '*'*40
        return self.hander(req)(env, start_response)
        #status = '200'
        #response_header = [('Content-type', 'text/plain')]
        #start_response(status, response_header)
        #return [self.name, time.ctime()]

    def hander(self, request):
        #print request, dir(request)
        method = request.method
        hander = getattr(self, method)
        print hander
        return hander(request)

    def PUT(self, request):
        file_name = request.headers['x-file-name']
        with open(file_name, 'wb') as f:
            n = 0
            while True:
                data = request.body_file.read(chunk_size)
                if not data:
                    break
                f.write(data)
                n += 1
        print 'after put write', n
        rs = Response()
        return rs

    def GET(self, request):
        file_name = request.headers['x-file-name']
        rs = Response()
        body_f = rs.body_file
        n = 0
        with open(file_name, 'rb') as f:
            n = 0
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                body_f.write(data)
                n += 1
        print 'after get write', n
        return rs


if __name__ == '__main__':
    app = Application('app1')
    run_wsgi(app, {'worker_count':10})


"""
使用curl来上传文件
curl -F upload=@./class_test.py http://127.0.0.1:8080
"""
