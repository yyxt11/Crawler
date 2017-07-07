# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.spiders import Spider
from xiaoshuo.items import XiaoshuoItem,DcontentItem,Chapterqueueloader
from xiaoshuo.SQL.DBhelper import dBhelper
from scrapy_redis.spiders import RedisCrawlSpider
from redis import Redis


class NovelCrawler(RedisCrawlSpider):
    name= 'Novel_slaver'
    redis_key ='NovelCrawler:chapter_url'


    def __init__(self,*args,**kwargs):
        domain = kwargs.pop('domain','')
        self.allowed_domans = filter(None,domain.split(','))
        super(NovelCrawler).__init__(*args,**kwargs)


    def parse(self, response):

        #确定分类
        el = Chapterqueueloader(item= DcontentItem,response=response)
        r = Redis()

        chaptercontent = response.xpath('//*[@id="contents"]/text()').extract()
        ALLcotent = '\n   '.join(chaptercontent)
        el.add_value('chaptercontent',ALLcotent)

        return el.load_item()







