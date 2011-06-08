#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re 

def network_mask(ip, netmask):
    """
    :param ip: inet address, exp: "192.168.1.1"
    :param netmask : netmask, exp: "255.255.255.0"
    :return network: network, exp: "192.168.1.0"
    """
    net_re = re.compile("\d{1,3}\.\d{1,3}\.\d{0,3}\.\d{0,3}")
    assert net_re.match(ip) and net_re.match(netmask)
    ip = [ int(x) for x in ip.split(".") ]
    netmask = [ int(x) for x in netmask.split(".") ]
    network = []
    for i in range(4):
        network.append( str(ip[i]&netmask[i]) )
    return ".".join(network)

print network_mask("192.168.1", "255.255.255.0")



