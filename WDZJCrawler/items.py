# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class WdzjcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TouyouItem(Item):
    # encoding: utf-8
    # 数据编码： utf-8
    userID = Field() #当前用户ID
    # userName = Field()
    friendshipType=Field()  #社交关系类型：Touy，即投友
    touyouID = Field()      # 投友ID
    touyouName = Field()    # 投友昵称
    collectionDate = Field()  #数据收集时间

class FanItem(Item):
    # encoding: utf-8
    # 数据编码： utf-8
    userID = Field() #当前用户ID
    friendshipType=Field() #社交关系类型：粉丝
    fanID = Field()        # 粉丝ID
    fanUserName=Field()    # 粉丝昵称
    collectionDate = Field()  # 数据收集时间


class UserInfoItem(Item):

    # basic informaton
    userID = Field()  #用户编号，数字
    userName = Field() #用户ID昵称
    p_level = Field() #用户等级，如v1，v2，管理员，禁止发言等
    role = Field()  #用户身份，如投资人
    score = Field() #用户积分

    # activity information
    Num_Friends = Field() # 投友数量
    # Num_Platforms = Field() #关注的平台数量
    Num_Fans = Field() # 粉丝数量
    Num_ColumnWriters = Field() # 专栏作家文章数
    Num_Collections = Field() #收藏


    # House Keeping information
    date = Field() #抓取数据的时间