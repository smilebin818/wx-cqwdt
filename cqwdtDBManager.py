#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import CqwdtDBManager

import entityInfo


def select_station_by_station_name(station_name):
    dbMgr = CqwdtDBManager("cqwdt")

    stationList = dbMgr.select_station_by_station_name(station_name)

    if len(stationList) == 0:
        dict_for_return[entityInfo.CODE] = entityInfo.FROMDBSETECT_ZERO

    elif len(stationList) > 0:
        dict_for_return['station_list'] = stationList
        dict_for_return[entityInfo.CODE] = entityInfo.FROMDBSETECT_MORE

    dbMgr.closeDB()

    return dict_for_return

def select_station_like_station_name(station_name):
    dbMgr = CqwdtDBManager("cqwdt")

    stationList = dbMgr.select_station_like_station_name(station_name)

    if len(stationList) == 0:
        dict_for_return[entityInfo.CODE] = entityInfo.FROMDBSETECT_ZERO

    elif len(stationList) == 1:
        dict_for_return['station_list'] = stationList
        dict_for_return[entityInfo.CODE] = entityInfo.FROMDBSETECT_ONE

    elif len(stationList) > 1:
        dict_for_return['station_list'] = stationList
        dict_for_return[entityInfo.CODE] = entityInfo.FROMDBSETECT_MORE

    dbMgr.closeDB()

    return dict_for_return
