#!/usr/bin/env python

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from xml.dom.minidom import parse, getDOMImplementation

def path(n):
    if n.nodeType == n.DOCUMENT_NODE:
        return list()
    elif n.nodeType == n.ELEMENT_NODE:
        return path(n.parentNode) + [n.nodeName,]
    else:
        return path(n.parentNode)

def collect(n, target_path, newdom):
    if path(n)[-len(target_path):] == target_path:
        newsubtree = newdom.importNode(n, True)
        newdom.documentElement.appendChild(newsubtree)
    else:
        for child in n.childNodes:
            collect(child, target_path, newdom)

if len(sys.argv) <= 1:
    print 'Usage: {} p1 p2 ... pn < input.xml'.format(sys.argv[0])
    print 'Prints out subtrees under //p1/p2/.../pn (where n >= 1) in input.xml'
    sys.exit(1)
dom = parse(sys.stdin)
newdom = getDOMImplementation().createDocument(None, 'result', None)
collect(dom, sys.argv[1:], newdom)
print newdom.toprettyxml()
