#!/usr/bin/env python
#coding:utf-8
"""
http://hi.baidu.com/isno/blog/item/32899358e2a6a4d99d820419.html

为了确认super的用法

注意下面，我在类D里面调用了super(D, self).show()后，
类C里面的super(C, self).__init__()就没有被执行了

这里super(C, self)应该是一个非绑定方法，这样做有一顶的危害，
比如影响了C中的super(C, self).__init__()的调用执行。

如果没有show()的调用，A.__init__()会被调用两次，
"""
class A(object):
    def __init__(self, arg):
        print "enter A"
        self.role = arg
        if arg is None:
            print 'arg is None'
        print "leave A"

    def show(self):
        print 'i am %s'%(self.role)

class B(object):
    def __init__(self):
        print "enter B"
        print "leave B"

class C(A):
    def show(self):
        print 'i am c'
        super(C, self).show()


class D(A):
    def __init__(self):
        print "enter D"
        A.__init__('ABC')
        print "leave D"

class E(B, C):
    def __init__(self):
        print "enter E"
        B.__init__(self)
        C.__init__(self)
        print "leave E"

class F(E, D):
    def __init__(self):
        print "enter F"
        E.__init__(self)
        D.__init__(self)
        print "leave F"

if __name__ == '__main__':
    #f = F()
    c = C('abc')
    c.show()

