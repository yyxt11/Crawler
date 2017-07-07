# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.spiders import Spider
from xiaoshuo.items import XiaoshuoItem,DcontentItem,Chapterqueueloader
from xiaoshuo.SQL.DBhelper import dBhelper
from scrapy_redis.spiders import RedisCrawlSpider
from redis import Redis


class NovelCrawler(RedisCrawlSpider):
    name= 'Novel_master'
    dbpointer = dBhelper()
    redis_key ='NovelCrawler:Novel_url'



    def __init__(self,*args,**kwargs):
        domain = kwargs.pop('domain','')
        self.allowed_domans = filter(None,domain.split(','))
        super(NovelCrawler).__init__(*args,**kwargs)
        self.url = 'http://www.23us.com/class/1_1.html'

    def parse(self, response):
        #//*[@id="content"]/dd[1]/table/tbody
        #确定分类
        r = Redis()
        catagory = response.xpath('//dl[@id="content"]/dt/h2/text()').re(u'(.+) - 文章列表')[0]
        for sel in response.xpath('//dl[@id="content"]/dd/table/tr[@bgcolor="#FFFFFF"]'):
            el = Chapterqueueloader(item=XiaoshuoItem,response=response)
            name = sel.xpath('./td[1]/a[2]/text()').extract()[0]
            author = sel.xpath('./td[4]/text()').extract()[0]
            novelurl = sel.xpath('./td[2]/a/@href').extract()[0]
            serialstatus = sel.xpath('./td[6]/text()').extract()[0]
            wordsnum = sel.xpath('./td[4]/text()').extract()[0]
            set = novelurl.split('/')
            serialnum = set[len(set)-2]
            """ 
            Item["name"] = name
            Item["author"] = author
            Item["novelurl"] = novelurl
            Item["serialstatus"] = serialstatus
            Item["wordsnum"] = wordsnum
            Item["serialnum"] = serialnum
            Item["category"] = catagory

            yield Item
            yield scrapy.Request(url=novelurl,callback = self.novel_get_parse,meta={'serial_id':serialnum})
            """
            r.lpush('NovelCrawler:Novel_url',novelurl)
            el.add_value('name',name)
            el.add_value('author',author)
            el.add_value('novelurl', novelurl)
            el.add_value('serialstatus', serialstatus)
            el.add_value('wordsnum', wordsnum)
            el.add_value('serialnum', serialnum)
            el.add_value('category', catagory)
            yield el.load_item()

        next_page = response.xpath('//dd[@class="pages"]/div/a[@class="next"]/@href').extract()[0] #获取下一页地址
        if next_page:
            yield scrapy.Request(next_page)



    def novel_get_parse(self,response):
        num = 0
        currenturl = response.url
        el = Chapterqueueloader(item=DcontentItem, response= response)
        r = Redis()
        for chapterline in response.xpath('//tr'):
           for url in chapterline.xpath('./td[@class="L"]'):
                num +=1

                urllist = url.xpath('.//a/@href').extract()
                if urllist:
                    relativeurl = urllist[0]
                else:
                    continue

                chapterurl = '%s%s' % (currenturl, relativeurl)

                urllist = url.xpath('.//a/text()').extract()
                if urllist:
                    chaptername = urllist[0]
                else:
                    continue

                r.lpush('NovelCrawler:chapter_url',chapterurl)
                time.sleep(0.5)
                el.add_value('serial_num',response.meta['serial_id'])
                el.add_value('sectionnum',num)
                el.add_value('chaptername',chaptername)
                el.add_value('chapterurl',chapterurl)

                yield el.load_item()


                #数据库查询章节是否重复
           #     ret = self.dbpointer.select_chapter(chapter_url=chapterurl)
           #     if(ret):
           #         print("***********************chapter is already existing")
           #         pass
           #     else:
           #         yield scrapy.Request(url=chapterurl, callback= self.chapter_get_parse,meta={'serial_num':response.meta['serial_id'],
           #                                                                                 'sectionnum': num,
           #                                                                                 'chaptername':chaptername,
           #                                                                                 'chapterurl':chapterurl})






