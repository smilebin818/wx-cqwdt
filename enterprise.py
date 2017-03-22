#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wechat_sdk import WechatBasic
from cgi import parse_qs, escape

import urllib, urllib2
import json

import entityInfo
import cqwdtDBManager

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

    # 解析用户信息
    wechat.parse_data(getRequestBody(environ))

    # 获得的用户输入信息
    text_from_user = wechat.message.content.encode("utf-8")

    # 返回给用户的信息
    text_to_user = ""
    
    # 用户信息中是否包含“到”的关键字
    stationList = text_from_user.split(entityInfo.direction_key.encode("utf-8"))

    # 单一站点，返回用户该站点的首末班时刻表
    if len(stationList) == 1:
        text_to_user = getInfoToUser(stationList[0].strip())

    # 站点到站点：红旗河沟到光电园  返回换乘路径（调用百度API）
    else:
        text_to_user = "站点到站点的功能\n目前还在调试中"

    text_to_user = wechat.response_text(text_to_user, "true")

    return text_to_user.encode("utf-8")


def getInfoToUser(text):
    return_text = ""

    # 根据用户输入的信息进行数据库查询该站名是否存在，并返回对应的车站信息
    station_name_result = cqwdtDBManager.select_station_by_station_name(text)

    rows_for_return = []

    # 返回结果为零件
    if station_name_result[entityInfo.CODE] == FROMDBSETECT_ZERO:
        # 进行模糊查询
        sel_station_like_name_return = cqwdtDBManager.select_station_like_station_name(text)

        if sel_station_like_name_return[entityInfo.CODE] == FROMDBSETECT_ZERO:
            # 利用图灵机器人进行对话
            return_text = tuling(text_from_user)

        if sel_station_like_name_return[entityInfo.CODE] == FROMDBSETECT_ONE:
            # 如果有一个匹配的站点，就将该站点进行返回
            stationList = station_name_result['station_list']
            station_name = stationList[0]["station_name"]

            # 回调自身函数查询该站点的信息
            getInfoToUser(station_name)

        elif sel_station_like_name_return[entityInfo.CODE] == FROMDBSETECT_MORE:
            # 编辑多件站点返回给用户，让用户确认输入完整站名
            stationList = station_name_result['station_list']

            rows_for_return.append("请输入完整的站名,参考如下：\n")

            for station_info in stationList:
                #station_info = list(station_info)

                rows_for_return.append(station_info["station_id"])
                rows_for_return.append(":")
                rows_for_return.append(station_info["station_name"])
                rows_for_return.append("\n")

            return_text = return_text.json(rows_for_return)

    # 返回结果为一件或者多件的场合
    elif station_name_result[entityInfo.CODE] == FROMDBSETECT_MORE:
        # 查询该站名的首末班车
        stationList = station_name_result['station_info']

        rows_for_return.append("车站名: {0}\n".format(text))

        for station_info in stationList:
            rows_for_return.append("-----------------\n")
            rows_for_return.append("列车线: {0}{1}\n".format(station_info["city"], station_info["metro"]))
            rows_for_return.append("方向　: {0}\n".format(station_info["direction"]))
            rows_for_return.append("首班车: {0}\n".format(station_info["weekday_first_time"]))
            rows_for_return.append("末班车: {0}\n".format(station_info["weekday_last_time"]))

        return_text = return_text.json(rows_for_return)

    return return_text

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

def tuling(text):
    url = "http://www.tuling123.com/openapi/api?key=77aa5b955fcab122b096f2c2dd8434c8&info={0}".format(text)
    content = urllib2.urlopen(url)
    content = json.loads(content.read())

    return content["text"]

# def createMenu():

    # 获取 access_token
    # getAccessToken = wechat.get_access_token()

    # access_token = getAccessToken.get('access_token', None)
    # access_token = access_token[0] if access_token else access_token

    # wechat.create_menu(entityInfo.menu_data)
