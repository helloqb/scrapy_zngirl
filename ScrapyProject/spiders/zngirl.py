# -*- coding: utf-8 -*-
import scrapy


class ZngirlSpider(scrapy.Spider):
    name = 'zngirl'
    allowed_domains = ['zngirls.com']
    start_urls = ['http://zngirls.com/']

    def parse(self, response):
        pass
