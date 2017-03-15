#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wechat_sdk import WechatBasic
from cgi import parse_qs, escape

import entityInfo

# 实例化 WechatBasic 官方接口类
wechat = WechatBasic(conf=entityInfo.conf)

# 微地铁的业务逻辑处理函数
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])

    # 腾讯服务器通过get请求给我们服务器
    # Python语言通过“QUERY_STRING”获取，并通过方法(parse_qs)转换成字典(d)
    d = parse_qs(environ['QUERY_STRING'])

    # 取得
    signature = d.get('signature', None)   # 微信加密签名
    timestmap = d.get('timestmap', None)   # 时间戳
    nonce     = d.get('nonce', None)       # 随机数
    echostr   = d.get('echostr', None)     # 随机字符串 (返回给腾讯进行token验证用)

    signature = signature[0] if signature else signature
    timestmap = signature[0] if signature else signature
    nonce     = signature[0] if signature else signature
    echostr   = signature[0] if signature else signature

    # 验证服务器地址的有效性
    if wechat.check_signature(signature, timestmap, nonce):
        # do OK thing
        print "验证服务器地址的有效性(成功)"  

        createMenu()

        return echostr
    else:
        # do err process
        print "验证服务器地址的有效性(失败)"    

        return None

def createMenu():

    # 获取 access_token
    # getAccessToken = wechat.get_access_token()

    # access_token = getAccessToken.get('access_token', None)
    # access_token = access_token[0] if access_token else access_token

    wechat.create_menu(entityInfo.menu_data)
