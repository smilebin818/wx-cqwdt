#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import CqwdtDBManager
from pypinyin import pinyin, lazy_pinyin

import entityInfo


def select_station_by_station_name(station_name):
    dict_for_return = []

    dbMgr = CqwdtDBManager("cqwdt")

    stationList = dbMgr.select_station_by_station_name(station_name)

    if len(stationList) == 0:
        # 中文转拼音
        stationPyList = lazy_pinyin(unicode(station_name))
        stationPy = "".join(stationPyList)

        stationList = dbMgr.select_station_by_station_py(stationPy)

    dbMgr.closeDB()

    return dict(station_list = stationList)

def select_station_like_station_name(station_name):
    dbMgr = CqwdtDBManager("cqwdt")

    stationList = dbMgr.select_station_like_station_name(station_name)

    # if len(stationList) == 0:
    #     dict_for_return[entityInfo.CODE] = entityInfo.FROMDBSETECT_ZERO

    # elif len(stationList) == 1:
    #     dict_for_return['station_list'] = stationList
    #     dict_for_return[entityInfo.CODE] = entityInfo.FROMDBSETECT_ONE

    # elif len(stationList) > 1:
    #     dict_for_return['station_list'] = stationList
    #     dict_for_return[entityInfo.CODE] = entityInfo.FROMDBSETECT_MORE

    dbMgr.closeDB()

    return dict(station_list = stationList)
