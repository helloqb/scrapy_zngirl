# -*- coding: utf-8 -*-
import hashlib

from scrapy.utils.python import to_bytes
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request


class ScrapyprojectPipeline(object):
    def process_item(self, item, spider):
        return item


# 重写 ImagesPipeline 类
# 重写 get_media_requests 方法请求url
# 重写 file_path 方法设置存放路径
class DefineFilePathImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        headers = {
            "Referer": item['referer'],
            # 'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
        }
        # 下载图片带 headers 才能成功, 否则视为盗链
        # 传输item 用于文件夹命名
        for u in item['img_url']:
            return Request(u, headers=headers, meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        # 将传递过来的 title ,创建新文件夹,实现图片按文件夹分类
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        item = request.meta['item']
        title = item['title']
        return f'full/{title}/{image_guid}.jpg'
