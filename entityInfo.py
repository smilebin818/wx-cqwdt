#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wechat_sdk import WechatConf

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

# 方向性文字 比如：光电园到花卉园
direction_key = u"到"



# 返回结果用的Key
CODE = "code"

# 根据车站名称进行数据库查询 返回CODE
FROMDBSETECT_ZERO   = 4001 # 返回结果为零件的对应CODE
FROMDBSETECT_ONE    = 1000 # 返回结果为一件的对应CODE
FROMDBSETECT_MORE   = 1001 # 返回结果为多件的对应CODE

# menu_data = {
#     'button':[
#         {
#             'type': 'click',
#             'name': '今日歌曲',
#             'key': 'V1001_TODAY_MUSIC'
#         },
#         {
#             'type': 'click',
#             'name': '歌手简介',
#             'key': 'V1001_TODAY_SINGER'
#         },
#         {
#             'name': '菜单',
#             'sub_button': [
#                 {
#                     'type': 'view',
#                     'name': '搜索',
#                     'url': 'http://www.soso.com/'
#                 },
#                 {
#                     'type': 'view',
#                     'name': '视频',
#                     'url': 'http://v.qq.com/'
#                 },
#                 {
#                     'type': 'click',
#                     'name': '赞一下我们',
#                     'key': 'V1001_GOOD'
#                 }
#             ]
#         }
#     ]
# }