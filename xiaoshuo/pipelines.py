# -*- coding: utf-8 -*-


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from xiaoshuo.items import XiaoshuoItem, DcontentItem
from xiaoshuo.SQL.DBhelper import dBhelper

class XiaoshuoPipeline(object):
    def __init__(self):
        self.dbpointer = dBhelper()
    def process_item(self, item, spider):


        if isinstance(item,XiaoshuoItem):
            print('======================================novel get')
            name = item['name']
            #数据库去重
            ret = self.dbpointer.select_novel(xs_name=name)
            if(ret):
                print('****************************novel is already existing')
                pass
            else:
                novel_name= item['name']
                novel_author = item['author']
                novel_serialnum = item['serialnum']
                novel_catagory = item["category"]
                self.dbpointer.insert_novel(xs_name=novel_name,
                                       xs_author=novel_author,
                                      xs_category=novel_catagory,
                                      xs_serial=novel_serialnum
                                      )
                print("=========new novel：%s saved" %novel_name)



        if isinstance(item,DcontentItem):
            novel_num = item['serial_num']
            chapter_content = item['chaptercontent']
            chapter_url = item['chapterurl']
            chapter_name = item['chaptername']
            chapter_sectionnum = item['sectionnum']
            self.dbpointer.insert_chapter(chapter_name = chapter_name,

                                    chapter_content=chapter_content,
                                    novel_serialnum=novel_num,
                                    sectionnum=chapter_sectionnum,
                                    chapter_url = chapter_url
                                    )
            print('=====================================chapter saved')
        return item


