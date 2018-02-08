# -*- coding: utf-8 -*-
import datetime
import json
import re
import scrapy
import time

from scrapy.loader import ItemLoader
from selenium import webdriver
from urllib import parse

from ArticleSpider.items import ZhihuQuestionItem, ZhihuAnswerItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{" \
                       "0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by" \
                       "%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment" \
                       "%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission" \
                       "%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked" \
                       "%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked" \
                       "%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29" \
                       "%5D.topics&limit={1}&offset={2} "
    captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def start_requests(self):
        # 利用浏览器进行知乎登录
        browser = webdriver.Chrome(executable_path='/Users/Arthur/Documents/chromedriver')
        browser.get('https://www.zhihu.com/signin')
        browser.find_element_by_css_selector('.SignFlow-accountInput.Input-wrapper input').send_keys('13611969835')
        browser.find_element_by_css_selector('.SignFlow-password .SignFlowInput .Input-wrapper input').send_keys(
            'zzh921223')
        browser.find_element_by_css_selector('.Button.SignFlow-submitButton').click()
        time.sleep(10)
        cookies = browser.get_cookies()
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, dont_filter=True, cookies=cookies)

    def parse(self, response):
        all_urls = response.css('a::attr(href)').extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith('https') else False, all_urls)
        for url in all_urls:
            match_obj = re.match('(.*zhihu.com/question/(\d+))($|/).*', url)
            if match_obj:
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)

    def parse_question(self, response):
        question_id = None
        # global question_id
        match_question_obj = re.match('(.*zhihu.com/question/(\d+))($|/).*', response.url)
        if match_question_obj:
            question_id = match_question_obj.group(2)

        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        item_loader.add_css('title', '.QuestionHeader-content h1.QuestionHeader-title::text')
        item_loader.add_value('url', response.url)
        item_loader.add_css('content', '.QuestionHeader-detail .RichText::text')
        item_loader.add_value('content', '')
        item_loader.add_value('zhihu_id', question_id)
        item_loader.add_css('answer_num', '.List-headerText span::text')
        item_loader.add_css('comments_num', '.QuestionHeader-Comment button::text')
        item_loader.add_css('watch_user_num', '.NumberBoard-itemValue::text')
        item_loader.add_css('click_num', '.NumberBoard-itemValue::text')
        item_loader.add_css('topics', '.QuestionHeader-topics .Popover div::text')

        question_item = item_loader.load_item()
        self.start_answer_url.format(question_id, 20, 0)

        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=self.headers,
                             callback=self.parse_answer)
        yield question_item

    def parse_answer(self, response):
        answer_json = json.loads(response.text)
        # is_end = answer_json['paging']['is_end']
        # next_url = answer_json['paging']['next']
        for answer in answer_json['data']:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["praise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        # if not is_end:
        #     yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)
