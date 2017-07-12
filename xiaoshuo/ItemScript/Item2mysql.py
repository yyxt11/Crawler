#coding=utf-8
import pymysql
import redis
import json
from xiaoshuo.SQL.DBhelper import dBhelper


def process_item():
    Redis_conn=redis.StrictRedis(host='localhost',port=6379,db=0)
    dbpointer = dBhelper()
    while True:
        source,data=Redis_conn.blpop("NovelCrawler:items")
        data=eval(data.decode("utf-8"))
        if type(data) == type({}):
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