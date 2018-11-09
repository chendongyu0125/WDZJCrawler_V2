# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.http import FormRequest
import json
from lxml import etree
import re
from WDZJCrawler.items import TouyouItem

class CrawtouyouSpider(scrapy.Spider):
    name = 'CrawlTouyou'
    allowed_domains = ['member.wdzj.com']
    # start_urls = ['http://member.wdzj.com/']
    def start_requests(self):
        ajaxURL = "https://member.wdzj.com/space/ajaxMore"
        return [FormRequest(ajaxURL, formdata={"uid": str(userID), "type": "touy", "page": '1'},
                            callback= lambda response, formdata={"uid": str(userID), "type": "touy", "page": '1'}, ajaxURL=ajaxURL:
                            self.parse_AjaxMorePage(response, formdata, ajaxURL), dont_filter=True) for userID in range(1, 1790000)]

        # return [FormRequest(ajaxURL, formdata={"uid": str(userID), "type": "touy", "page": '1'},
        #                     callback= lambda response, formdata={"uid": str(userID), "type": "touy", "page": '1'}, ajaxURL=ajaxURL:
        #                     self.parse_AjaxMorePage(response, formdata, ajaxURL), dont_filter=True) for userID in range(1, 40000)]


    def parse(self, response):
        pass

    def parse_AjaxMorePage(self, response, formdata, ajaxURL):  #将ajaxURL，以及当前用户ID等信息传递给处理函数
        '''
             @url https://member.wdzj.com/space/ajaxMore
             @returns items 1
             @scrapes userID, touyouID, friendshipType, collectionDate

             :param response:
             :return:
        '''

        userID = formdata['uid']
        currentPage=int(formdata['page'])
        friendshipType=formdata['type']

        js = json.loads(response.body)



        ajaxHtml = js['ajaxHtml'] # 如果没有返回任何数据，说明该用户没有投友
        if len(ajaxHtml) ==0:
            return

        htmlPage=js['htmlPage']

        selector = etree.HTML(ajaxHtml)
        touyous = selector.xpath('//li')

        for touyou in touyous:

            touyouNameInfo=touyou.xpath(".//div[contains(@class,'plt-uName')]/a/text()") #如果包含的投友Name信息有效
            if len(touyouNameInfo) >0:
                touyouItem = TouyouItem()
                touyouName = touyou.xpath(".//div[contains(@class,'plt-uName')]/a/text()")[0]
                regx = re.compile(r"https://member.wdzj.com/space-([\d]+).html")
                touyouID = regx.findall(touyou.xpath(".//div[contains(@class,'plt-uName')]/a/@href")[0])[0]
                touyouItem['userID'] = userID
                touyouItem['friendshipType'] = friendshipType
                touyouItem['touyouID']=touyouID
                touyouItem['touyouName']=touyouName
                touyouItem['collectionDate'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield touyouItem
        if htmlPage=="show":  #说明还有更多页面
            formdata = {"uid": userID, "type": "touy", "page": str(currentPage + 1)}
            yield FormRequest(ajaxURL, formdata=formdata,
                              callback=lambda response, formdata=formdata, ajaxURL=ajaxURL: self.parse_AjaxMorePage(response, formdata, ajaxURL), dont_filter=True)

