#coding=utf-8
import pymysql
import redis
import json
from xiaoshuo.SQL.DBhelper import dBhelper
from xiaoshuo.spiders.IgnoreFilter import IgnoreItem

"""
import sys 
if not "C:/Users/mochy-MD92/Documents/AppSpider/xiaoshuo/xiaoshuo/SQL/" in sys.path:
    sys.path.append("C:/Users/mochy-MD92/Documents/AppSpider/xiaoshuo/xiaoshuo/SQL/") 
if not 'DBhelper' in sys.modules:
    b = __import__('DBhelper')
else:
    eval('import DBhelper')
    b = eval('reload(DBhelper)')
"""
def process_item():
    Filterpointer = IgnoreItem()
    Redis_conn=redis.StrictRedis(host='localhost',port=6379,db=0)
    dbpointer = dBhelper()
    while True:
        source,data=Redis_conn.blpop("NovelCrawler:items")
        data=eval(data.decode("utf-8"))
        if type(data) == type({}):
            #防止重复插入
            chapterurl = data['chapterurl']
          #  if Filterpointer.filter(chapterurl):
            dbpointer.insert_chapter(chapter_name=data['chaptername'],
                                     chapter_content=data['chaptercontent'],
                                     novel_serialnum=data['serial_num'],
                                     sectionnum=data['sectionnum'],
                                     chapter_url=data['chapterurl']
                                     )
            print('=====================================chapter saved')

        else:
            print('==========数据不是dict========')






#测试
if __name__=="__main__":
    process_item()