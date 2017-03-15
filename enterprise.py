#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wechat_sdk import WechatBasic
from cgi import parse_qs, escape

import entityInfo

wechat = WechatBasic(conf=entityInfo.conf)

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])

    d = parse_qs(environ['QUERY_STRING'])

    print d

    signature = d.get('signature', None)
    timestmap = d.get('timestmap', None)
    nonce = d.get('nonce', None)
    echostr = d.get('echostr', None)

    if wechat.check_signature(signature, timestmap, nonce):
        # do OK thing
        createMenu()
    else:
        # do err process
        print "fuck you, some went wrong"    

    return "hello world"


def createMenu():
    wechat.create_menu(entityInfo.menu_data)
