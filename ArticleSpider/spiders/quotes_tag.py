# -*- coding: utf-8 -*-
import scrapy
from urllib import parse


class QuotesTagSpider(scrapy.Spider):
    name = 'quotes_tag'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def __init__(self, stats):
        print(stats)
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def parse(self, response):
        self.logger.info(response.url)
        for quote in response.css('span.tag-item'):
            tag_url = quote.css('a::attr(href)').extract_first()
            yield scrapy.Request(parse.urljoin(response.url, tag_url), callback=self.parse_tag)

    def parse_tag(self, response):
        self.logger.info(response.url)
        for quote in response.css('div.quote'):
            print({'text': quote.css('span.text::text').extract_first(),
                   'author': quote.css('small.author::text').extract_first()})

            next_page = response.css('li.next a::attr(href)').extract_first()
            if next_page is not None:
                yield response.follow(next_page, self.parse_tag)
