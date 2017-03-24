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
    
    stationList = []

    # 用户信息中是否包含“到”
    if entityInfo.direction_key_1.encode("utf-8") in text_from_user:
        stationList = text_from_user.split(entityInfo.direction_key_1.encode("utf-8"))
    # 用户信息中是否包含“至”
    elif entityInfo.direction_key_2.encode("utf-8") in text_from_user:
        stationList = text_from_user.split(entityInfo.direction_key_2.encode("utf-8"))
    # 用户信息中是否包含“TO”
    elif entityInfo.direction_key_3.encode("utf-8") in text_from_user.upper():
        stationList = text_from_user.upper().split(entityInfo.direction_key_3.encode("utf-8"))
    else:
        stationList = text_from_user.split(entityInfo.direction_key_1.encode("utf-8"))

    # 单一站点，返回用户该站点的首末班时刻表
    if len(stationList) == 1:
        text_to_user = getInfoToUser(stationList[0].strip())

    # 站点到站点：红旗河沟到光电园  返回换乘路径（调用百度API）
    elif len(stationList) == 2:
        text_to_user = getStationToStationInfo(stationList[0], stationList[1])

    # 用户输入多个关键字的时候返给用户信息：
    elif len(stationList) > 2:
        text_to_user = "查询站点到站点的规则:\n①\"A站\" 到 \"B站\"\n　②\"A站\" 至 \"B站\"\n　③\"A站\" to \"B站\"\n例： 茶园到光电园"

    text_to_user = wechat.response_text(text_to_user, "true")

    return text_to_user.encode("utf-8")

# 查询站点到站点的换乘路径
def getStationToStationInfo(startStation, lastStation):
    return_text = ""
    originGeo = ""
    destinationGeo = ""

    startStationGeoReturn = getGeo(startStation, 0)

    return_flg = startStationGeoReturn["return_flg"]
    if return_flg :
        originGeo = startStationGeoReturn["geo"]
        startStation = startStationGeoReturn["station_name"]
    else:
        return startStationGeoReturn["massage_text"]

    lastStationGeoReturn = getGeo(lastStation, 1)

    return_flg = lastStationGeoReturn["return_flg"]
    if return_flg :
        destinationGeo = lastStationGeoReturn["geo"]
        lastStation = lastStationGeoReturn["station_name"]
    else:
        return lastStationGeoReturn["massage_text"]

    origin = entityInfo.baidu_origin.format(originGeo)
    destination = entityInfo.baidu_destination.format(destinationGeo)
    baidu_url = entityInfo.baidu_url.format(origin, destination)

    content = urllib2.urlopen(baidu_url)
    content = json.loads(content.read())

    if content['status'] == 0:

        start_station = ""
        last_station = ""
        rows_for_return = []

        routesList = content["result"]["routes"]

        if routesList :
            steps = routesList[0]["steps"]

            rows_for_return.append("路　线: {0}⇒{1}\n".format(startStation, lastStation))
            rows_for_return.append("====================\n")

            for i in range(len(steps)):
                vehicle_info = steps[i][0]["vehicle_info"]

                if vehicle_info["type"] == 3:
                    detail = vehicle_info["detail"]

                    #print u"首班车:{0}".format(detail["first_time"])
                    #print u"末班车:{0}".format(detail["last_time"])
                    rows_for_return.append("出发站: {0}\n".format(textToUTF8(detail["on_station"])))
                    rows_for_return.append("到达站: {0}\n".format(textToUTF8(detail["off_station"])))
                    rows_for_return.append("经过站: {0} 站\n".format(textToUTF8(detail["stop_num"])))
                    rows_for_return.append("轨道线: {0}\n".format(textToUTF8(detail["name"])))

                if (vehicle_info["type"] == 5) and (i != 0):
                    detail = vehicle_info["detail"]

                    rows_for_return.append("--------------------\n")
                    rows_for_return.append(textToUTF8(steps[i][0]["instructions"]))
                    rows_for_return.append("\n")
                    rows_for_return.append("--------------------\n")

                return_text = "".join(rows_for_return)

    elif content['status'] == 1:
        print "服务器内部错误"
    elif content['status'] == 2:
        print "参数无效"
    elif content['status'] == 1001:
        print "没有公交方案"
    elif content['status'] == 1002:
        print "没有匹配的POI"

    return return_text

# 得到站点的经纬度
def getGeo(station, station_flg):

    ret = {}
    rows_for_return = []

    stationByNameResult = cqwdtDBManager.select_station_by_station_name(station)

    stationList = stationByNameResult['station_list']

    # 返回结果为零件
    if len(stationList) == 0:
        # 进行模糊查询
        stationLikeNameReturn = cqwdtDBManager.select_station_like_station_name(station)

        stationLikeList = stationLikeNameReturn['station_list']

        if len(stationLikeList) == 0:

            if station_flg == 0:
                rows_for_return.append("起点站: {0}\n".format(station))
            else:
                rows_for_return.append("终点站: {0}\n".format(station))

            rows_for_return.append("--------------------\n")
            rows_for_return.append("※没有查询到该站点\n")
            rows_for_return.append("※确认站点名后再试\n")

            # 查询没有结果
            ret["return_flg"] = 0
            ret["massage_text"] = "".join(rows_for_return)
        
        # 如果有一个匹配的站点，返回该站点的信息（经纬度）
        elif len(stationLikeList) == 1:
            if int(stationLikeList[0]["open_traffic"]) == 0:
                if station_flg == 0:
                    rows_for_return.append("起点站: {0}\n".format(station))
                else:
                    rows_for_return.append("终点站: {0}\n".format(station))

                rows_for_return.append("--------------------\n")
                #rows_for_return.append("列车线: {0}{1}\n".format(station_info["city"], station_info["metro"]))
                rows_for_return.append("※该站点目前尚未开通\n")
                rows_for_return.append("※输入附近站点再查询")

                # 查询没有结果
                ret["return_flg"] = 0
                ret["massage_text"] = "".join(rows_for_return)

            else:
                ret["station_name"] = stationLikeList[0]["station_name"]
                ret["return_flg"] = 1
                ret["geo"] = stationLikeList[0]["geo"]

        elif len(stationLikeList) > 1:
            stationLikeNewList = getNotIterateList(stationLikeList)

            if len(stationLikeNewList) == 1:
                ret["station_name"] = stationLikeNewList[0]["station_name"]
                ret["return_flg"] = 1
                ret["geo"] = stationLikeNewList[0]["geo"]
            else:
                if station_flg == 0:
                    rows_for_return.append("起点站\"{0}\"太模糊\n".format(station))
                else:
                    rows_for_return.append("终点站\"{0}\"太模糊\n".format(station))

                rows_for_return.append("※请确认你要输入的车站\n")
                rows_for_return.append("--------------------\n")

                for station_info in stationLikeList:
                    #station_info = list(station_info)

                    rows_for_return.append(station_info["station_id"])
                    rows_for_return.append(": ")
                    rows_for_return.append(station_info["station_name"])
                    rows_for_return.append("\n")

                # 查询没有结果
                ret["return_flg"] = 0
                ret["massage_text"] = "".join(rows_for_return)

    # 返回结果为一件或者多件的场合，返回第一件的经纬度即可
    elif len(stationList) > 0:
        if int(stationList[0]["open_traffic"]) == 0:

            if station_flg == 0:
                rows_for_return.append("起点站: {0}\n".format(station))
            else:
                rows_for_return.append("终点站: {0}\n".format(station))

            rows_for_return.append("--------------------\n")
            #rows_for_return.append("列车线: {0}{1}\n".format(station_info["city"], station_info["metro"]))
            rows_for_return.append("※该站点目前尚未开通\n")
            rows_for_return.append("※输入附近站点再查询")

            # 查询没有结果
            ret["return_flg"] = 0
            ret["massage_text"] = "".join(rows_for_return)

        else:
            ret["station_name"] = station
            ret["return_flg"] = 1
            ret["geo"] = stationList[0]["geo"]

    return ret

# 查询首末班车时刻
def getInfoToUser(text):
    return_text = ""
    rows_for_return = []

    # 根据用户输入的信息进行数据库查询该站名是否存在，并返回对应的车站信息
    stationByNameResult = cqwdtDBManager.select_station_by_station_name(text)

    stationList = stationByNameResult['station_list']

    # 返回结果为零件
    if len(stationList) == 0:
        # 进行模糊查询
        stationLikeNameReturn = cqwdtDBManager.select_station_like_station_name(text)

        stationLikeList = stationLikeNameReturn['station_list']

        if len(stationLikeList) == 0:
            # 利用图灵机器人进行对话
            return_text = tuling(text)

        if len(stationLikeList) == 1:
            # 如果有一个匹配的站点，就将该站点进行返回
            station_name = stationLikeList[0]["station_name"]

            # 回调自身函数查询该站点的信息
            return getInfoToUser(station_name)

        elif len(stationLikeList) > 1:
            # 判断模糊查询出来的结果是否是同一个站点： 例如(关键字[红旗]进行查询会出现 322：红旗河沟  612：红旗河沟)
            stationNewList = getNotIterateList(stationLikeList)

            if len(stationNewList) == 1:
                station_name = stationNewList[0]["station_name"]
                # 回调自身函数查询该站点的信息
                return getInfoToUser(station_name)
            else:
                # 编辑多件站点返回给用户，让用户确认输入完整站名
                rows_for_return.append("请输入完整的站名,如下：\n")
                rows_for_return.append("--------------------\n")

                for station_info in stationLikeList:
                    #station_info = list(station_info)

                    rows_for_return.append(station_info["station_id"])
                    rows_for_return.append(": ")
                    rows_for_return.append(station_info["station_name"])
                    rows_for_return.append("\n")

            return_text = "".join(rows_for_return)

    # 返回结果为一件或者多件的场合
    elif len(stationList) > 0:
        # 返回该站名的首末班车
        rows_for_return.append("车站名: {0}\n".format(text))

        if int(stationList[0]["open_traffic"]) == 0:
            rows_for_return.append("--------------------\n")
            #rows_for_return.append("列车线: {0}{1}\n".format(station_info["city"], station_info["metro"]))
            rows_for_return.append("※该站点目前尚未开通")

            return_text = "".join(rows_for_return)

        else:
            for station_info in stationList:
                rows_for_return.append("--------------------\n")
                rows_for_return.append("列车线: {0}{1}\n".format(station_info["city"], station_info["metro"]))
                rows_for_return.append("方　向: {0}\n".format(station_info["direction"]))
                rows_for_return.append("首班车: {0}\n".format(station_info["weekday_first_time"]))
                rows_for_return.append("末班车: {0}\n".format(station_info["weekday_last_time"]))

            return_text = "".join(rows_for_return)

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

# 得到一个list里面不重复的数据
def getNotIterateList(stationList):
    d = {}
    ret = []

    for station in stationList:
        if station["station_name"] not in d:
            d[station["station_name"]] = True
            ret.append(station)
        else:
            pass

    return ret

def tuling(text):
    url = "http://www.tuling123.com/openapi/api?key=77aa5b955fcab122b096f2c2dd8434c8&info={0}".format(text)
    content = urllib2.urlopen(url)
    content = json.loads(content.read())

    return content["text"]

# 转码格式： UTF-8
def textToUTF8(text):
    if type(text) == type(u""):
        return text.encode("utf-8")
    else:
        return text
