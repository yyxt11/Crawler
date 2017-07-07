# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from xiaoshuo.items import XiaoshuoItem,DcontentItem
from xiaoshuo.SQL.DBhelper import dBhelper




class NovelCrawler(Spider):
    name= 'Novelcrawler'
    allowed_domains = [ ]
    dbpointer = dBhelper()
    start_urls = ['http://www.23us.com/class/1_1.html']



    def parse(self, response):
        print("==============render over===============================")
        #//*[@id="content"]/dd[1]/table/tbody
        #确定分类
        catagory = response.xpath('//dl[@id="content"]/dt/h2/text()').re(u'(.+) - 文章列表')[0]
        for sel in response.xpath('//dl[@id="content"]/dd/table/tr[@bgcolor="#FFFFFF"]'):
            Item = XiaoshuoItem()

            name = sel.xpath('./td[1]/a[2]/text()').extract()[0]
            author = sel.xpath('./td[4]/text()').extract()[0]
            novelurl = sel.xpath('./td[2]/a/@href').extract()[0]
            serialstatus = sel.xpath('./td[6]/text()').extract()[0]
            wordsnum = sel.xpath('./td[4]/text()').extract()[0]
            set = novelurl.split('/')
            serialnum = set[len(set)-2]

            Item["name"] = name
            Item["author"] = author
            Item["novelurl"] = novelurl
            Item["serialstatus"] = serialstatus
            Item["wordsnum"] = wordsnum
            Item["serialnum"] = serialnum
            Item["category"] = catagory

            yield Item
            yield scrapy.Request(url=novelurl,callback = self.novel_get_parse,meta={'serial_id':serialnum})

        next_page = response.xpath('//dd[@class="pages"]/div/a[@class="next"]/@href').extract()[0] #获取下一页地址
        if next_page:
            yield scrapy.Request(next_page)



    def novel_get_parse(self,response):
        num = 0
        currenturl = response.url
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


                #数据库查询章节是否重复
                ret = self.dbpointer.select_chapter(chapter_url=chapterurl)
                if(ret):
                    print("***********************capter is already existing")
                    pass
                else:
                    yield scrapy.Request(url=chapterurl, callback= self.chapter_get_parse,meta={'serial_num':response.meta['serial_id'],
                                                                                            'sectionnum': num,
                                                                                            'chaptername':chaptername,
                                                                                            'chapterurl':chapterurl})



    def chapter_get_parse(self,response):
        Item = DcontentItem()
        Item['serial_num'] = response.meta['serial_num']
        Item['sectionnum'] = response.meta['sectionnum']
        Item['chapterurl'] = response.meta['chapterurl']
        Item['chaptername'] = response.meta['chaptername']
        chaptercontent = response.xpath('//*[@id="contents"]/text()').extract()
        Item['chaptercontent'] = '\n   '.join(chaptercontent)



        return Item




