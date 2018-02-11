# -*- coding: utf-8 -*-
import json

import scrapy


class QingflowSpider(scrapy.Spider):
    name = 'qingflow'
    allowed_domains = ['qingflow.com']

    # start_urls = ['https://qingflow.com/']

    def start_requests(self):
        return [scrapy.Request(url='https://qingflow.com/api/user/login',
                               method='POST',
                               body=json.dumps({'email': 'arthur_zzh@126.com', 'password': 'zzh921223'}),
                               callback=self.logged_in,
                               headers={'Content-Type': 'application/json'})]

    def logged_in(self, response):
        resp = json.loads(response.text)
        yield scrapy.Request(url='https://qingflow.com/api/app?tagId=0&pageSize=20&pageNum=1',
                             headers={'token': resp['token'], 'wsId': 40005})

    def parse(self, response):
        print(response)
        pass
