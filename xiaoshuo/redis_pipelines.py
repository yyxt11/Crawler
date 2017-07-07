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
        data=json.loads(data.decode("utf-8"))

        dbpointer.insert_chapter(chapter_name=data['chapter_name'],
                                  chapter_content=data['chapter_content'],
                                  novel_serialnum=data['novel_num'],
                                  sectionnum=data['chapter_sectionnum'],
                                  chapter_url=data['chapter_url']
                                  )
        print('=====================================chapter saved')




#测试
    if __name__=="__main__":
        process_item()