# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from sched import scheduler
from scrapy.loader import ItemLoader
from scrapy.loader.processors import  MapCompose,TakeFirst,Join

class XiaoshuoItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()# 小说名
    author = scrapy.Field()# 作者
    novelurl = scrapy.Field()  # 小说地址
    serialstatus = scrapy.Field()# 状态
    wordsnum = scrapy.Field() # 连载字数
    category = scrapy.Field()  # 文章类别
    serialnum = scrapy.Field() # 小说编号


class DcontentItem(scrapy.Item):
    serial_num = scrapy.Field()         #小说编号
    chaptercontent = scrapy.Field()     #章节内容
    sectionnum = scrapy.Field()         #章节顺序
    chapterurl = scrapy.Field()         #章节地址
    chaptername = scrapy.Field()        #章节名字

# Item loader
#class Chapterqueueloader(ItemLoader):
#    default_input_processor = MapCompose(lambda s: s.strip())
#    default_output_processor = TakeFirst()
#    description = Join()