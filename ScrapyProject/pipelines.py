# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import functools
import hashlib
import six

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from PIL import Image

from scrapy.utils.misc import md5sum
from scrapy.utils.python import to_bytes
from scrapy.http import Request
from scrapy.settings import Settings
from scrapy.exceptions import DropItem
# TODO: from scrapy.pipelines.media import MediaPipeline
from scrapy.pipelines.files import FileException, FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.misc import md5sum


class ScrapyprojectPipeline(object):
    def process_item(self, item, spider):
        return item


# 重写ImagesPipeline 类
# 目前是直接将默认的 ImagePipeline 复制过来
# 重写 get_media_requests 方法请求url
# 重写 file_path 方法设置存放路径
class DefineFilePathImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        headers = {
            "Host": "www.nvshens.com",
            "Referer": item['referer'],
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
        }
        # 下载图片带 headers 才能成功, 否则视为盗链
        # 传输item 用于文件夹命名
        return [Request(x, headers=headers, meta={'item': item}) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)
        ## end of deprecation warning block

        # 将传递过来的 title ,创建新文件夹,实现图片按文件夹分类
        item = request.meta['item']
        title = item['title']
        image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        return 'full/%s/%s.jpg' % (title, image_guid)
