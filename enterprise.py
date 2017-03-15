#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wechat_sdk import WechatBasic
from cgi import parse_qs, escape

import entityInfo

def getRequestBody(environ):
    # the environment variable CONTENT_LENGTH may be empty or missing
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))

    except (ValueError):
        request_body_size = 0

    # When the method is POST the query string will be sent
    # in the HTTP request body which is passed by the WSGI server
    # in the file like wsgi.input environment variable.
    request_body = environ['wsgi.input'].read(request_body_size)

    return request_body

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
    timestamp = d.get('timestamp', None)   # 时间戳
    nonce     = d.get('nonce', None)       # 随机数
    echostr   = d.get('echostr', None)     # 随机字符串 (返回给腾讯进行token验证用)

    signature = signature[0] if signature else signature
    timestamp = timestamp[0] if timestamp else timestamp
    nonce     = nonce[0] if nonce else nonce
    echostr   = echostr[0] if echostr else echostr

    # 验证服务器地址的有效性
    if echostr:
        if wechat.check_signature(signature, timestamp, nonce):
            # do OK thing
            print "验证服务器地址的有效性(成功)"

            return echostr or ""
        else:
            # do err process
            print "验证服务器地址的有效性(失败)"

            return ""

    request_body = getRequestBody(environ)

    data = request_body # ['data']

    text_from_user = wechat.parse_data(data)

    text_to_user = wechat.response_text("开发不出来了，不要期待了。。。")

    return text_to_user.encode("utf-8")

def createMenu():

    # 获取 access_token
    # getAccessToken = wechat.get_access_token()

    # access_token = getAccessToken.get('access_token', None)
    # access_token = access_token[0] if access_token else access_token

    wechat.create_menu(entityInfo.menu_data)
