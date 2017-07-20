# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from xiaoshuo.scrapy_redis.BloomfilterOnRedis import BloomFilter
from scrapy.http import Request
from scrapy.utils.request import request_fingerprint
from scrapy import signals
import redis
import random

class XiaoshuoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self,response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self,response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


#随机UA头
class RandomUA(object):
    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
     return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        print("**************************" + random.choice(self.agents))
        request.headers.setdefault('User-Agent', random.choice(self.agents))

#boolfilter增量，利用redis持久性
class IgnoreItem(object):
    def __init__(self, host, port, db, key):
        self.host = host
        self.port = port
        self.db = db
        self.key = key
        self.server = redis.Redis(host=host, port=port, db=db)
        self.bf = BloomFilter(self.server, self.key, blockNum=1)  # you can increase blockNum if your are filtering too many urls

    @classmethod
    def from_crawler(cls, crawler):

        return cls(
            host= crawler.settings.get('INCREASE_HOST'),
            port= crawler.settings.get('INCREASE_PORT'),
            db = crawler.settings.get('INCREASE_DB'),
            key = crawler.settings.get('INCREASE_KEY'),
        )

    def process_spider_output(self, response, result, spider):
        def _filter(request):
            if isinstance(request, Request):
                fp = self.visited(response.request)
                if self.bf.isContains(fp):
                    return False
                else:
                    self.bf.insert(fp)
                    return True

            return True
        return (r for r in result or () if _filter(r))

    def visited(self, request):
        return request_fingerprint(request)

