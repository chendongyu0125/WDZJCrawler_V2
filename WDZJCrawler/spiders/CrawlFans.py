# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.http import FormRequest
import json
from lxml import etree
import re
from WDZJCrawler.items import FanItem

class CrawlfansSpider(scrapy.Spider):
    name = 'CrawlFans'
    allowed_domains = ['member.wdzj.com']
    # start_urls = ['http://http://member.wdzj.com/']
    def start_requests(self):
        ajaxURL = "https://member.wdzj.com/space/ajaxMore"
        return [FormRequest(ajaxURL, formdata={"uid": str(userID), "type": "fans", "page": '1'},
                            callback= lambda response, formdata={"uid": str(userID), "type": "fans", "page": '1'}, ajaxURL=ajaxURL:
                            self.parse_AjaxMorePage(response, formdata, ajaxURL), dont_filter=True) for userID in range(1, 1790000)]


    def parse(self, response):
        pass


    def parse_AjaxMorePage(self, response, formdata, ajaxURL):  #将ajaxURL，以及当前用户ID等信息传递给处理函数

        userID = formdata['uid']
        currentPage=int(formdata['page'])
        friendshipType=formdata['type']

        js = json.loads(response.body)



        ajaxHtml = js['ajaxHtml'] # 如果没有返回任何数据，说明该用户没有投友
        if len(ajaxHtml) ==0:
            return

        htmlPage=js['htmlPage']

        selector = etree.HTML(ajaxHtml)
        fans = selector.xpath('//li')

        for fan in fans:

            fanNameInfo=fan.xpath(".//div[contains(@class,'plt-uName')]/a/text()") #如果包含的投友Name信息有效
            if len(fanNameInfo) >0:
                fanItem = FanItem()
                fanName = fan.xpath(".//div[contains(@class,'plt-uName')]/a/text()")[0]
                regx = re.compile(r"https://member.wdzj.com/space-([\d]+).html")
                fanID = regx.findall(fan.xpath(".//div[contains(@class,'plt-uName')]/a/@href")[0])[0]
                fanItem['userID'] = userID
                fanItem['friendshipType'] = friendshipType
                fanItem['fanID']=fanID
                fanItem['fanUserName']=fanName
                fanItem['collectionDate'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield fanItem
        if htmlPage=="show":  #说明还有更多页面
            formdata = {"uid": userID, "type": "fans", "page": str(currentPage + 1)}
            yield FormRequest(ajaxURL, formdata=formdata,
                              callback=lambda response, formdata=formdata, ajaxURL=ajaxURL: self.parse_AjaxMorePage(response, formdata, ajaxURL), dont_filter=True)


