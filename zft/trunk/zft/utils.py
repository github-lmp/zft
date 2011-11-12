#!/usr/bin/env python
#coding: utf-8

def check_utf8(string):
     """
     Validate if a string is valid UTF-8.
     :param string: string to be validated
     :returns: True if the string is valid utf-8, False otherwise
     """
     try:
        string.decode('UTF-8')
        return True
     except UnicodeDecodeError:
        return False


