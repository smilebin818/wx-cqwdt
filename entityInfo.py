#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wechat_sdk import WechatConf

# ============================微信相关的定义 Start=====================================
myToken          = "smilebinToken"
myAppId          = "wx692ad34a8ba6feff"
myAppsecret      = "cabff21c726d3b2b2a9ae94d9daa039a"
myEncodingAESKey = "NyI5ok2QSd59c3MheyDfWpzHen3KmY3bwc8noyBkFHg"

conf = WechatConf(
    token='smilebinToken', 
    appid='wx692ad34a8ba6feff', 
    appsecret='cabff21c726d3b2b2a9ae94d9daa039a', 
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='NyI5ok2QSd59c3MheyDfWpzHen3KmY3bwc8noyBkFHg'  # 如果传入此值则必须保证同时传入 token, appid
)

# ============================微信相关的定义 End=======================================

# ============================百度地图相关的定义 Start==================================

baidu_origin = "origin={0}"
baidu_destination = "&destination={0}"
baidu_ak = "&ak=1ce6987ff4bbe857f40cfaf6b99cd050" 
baidu_url = "http://api.map.baidu.com/direction/v2/transit?{0}{1}&ak=1ce6987ff4bbe857f40cfaf6b99cd050"

# ============================百度地图相关的定义 End====================================

# ============================程序相关的定义 Start=====================================
# 方向性文字 比如：光电园到花卉园
direction_key_1 = u"到"
direction_key_2 = u"至"
direction_key_3 = u"TO"


# 返回结果用的Key
CODE = "code"

# 根据车站名称进行数据库查询 返回CODE
FROMDBSETECT_ZERO   = 4001 # 返回结果为零件的对应CODE
FROMDBSETECT_ONE    = 1000 # 返回结果为一件的对应CODE
FROMDBSETECT_MORE   = 1001 # 返回结果为多件的对应CODE

# ============================程序相关的定义 End=======================================