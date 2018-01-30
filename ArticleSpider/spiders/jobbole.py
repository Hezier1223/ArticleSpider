# -*- coding: utf-8 -*-
import scrapy
import re


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://www.importnew.com/27940.html']

    def parse(self, response):
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        pub_time_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0]
        match_re = re.match('.*(\d{4}/\d{2}/\d{2})', pub_time_list)
        if match_re:
            pub_time = match_re.group(1)
        content = response.xpath('//div[@class="entry"]').extract()[0]
        print(content)
