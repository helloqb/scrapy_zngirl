# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ScrapyProject.items import ScrapyprojectItem
from urllib import parse


class ZngirlSpider(scrapy.Spider):
    name = 'zngirl'
    allowed_domains = ['nvshens.net']
    # 爬虫开始地址, 女神个人主页
    # start_urls = ['file:////C:/Users/rui97/Desktop/1.html']
    start_urls = ['https://www.nvshens.net/girl/21745/album/']

    def parse(self, response):
        post_nudes = response.css('.igalleryli')
        for post_nude in post_nudes:
            # 获取每个套图 URL
            post_url = post_nude.css('.igalleryli_div a ::attr(href)').extract_first()
            # 获取套图名称
            title = post_nude.css('.igalleryli_title a ::text').extract_first()
            # title 采用 meta 传递, 用于下载图片时按文件夹进行分类
            yield Request(url=parse.urljoin(response.url, post_url), meta={'title': title}, callback=self.parse_detail)

    def parse_detail(self, response):
        img_item = ScrapyprojectItem()
        title = response.meta.get("title", "")
        # 单个图片 URL
        img_nudes = response.css('#hgallery img')
        img_urls = []
        for img_nude in img_nudes:
            img_url = img_nude.css('::attr(src)').extract_first()
            # 大图
            img_urls.append(img_url.replace('/s', ''))
        img_item['title'] = title
        img_item['img_url'] = img_urls
        img_item['referer'] = response.url
        yield img_item

        # 有下一页则继续
        # 该网站很鸡贼, 尾页是跳转至第一页, 不注意会一直重复循环单个套图,
        # 但是其第一页不是以'.html'结尾的,可以以此为依据
        next_url = response.css('#pages a.a1[href$=".html"]:contains("下一页")::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), meta={'title': title}, callback=self.parse_detail)
