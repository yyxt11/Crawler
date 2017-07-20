#=========================
#网页数据库交互类
#=========================
import web
from xiaoshuo.SQL.setting import DB_Config


db= web.database(dbn='mysql',\
                db =DB_Config['MYSQL_DBNAME'],\
                host=DB_Config['MYSQL_HOST'],\
                user=DB_Config['MYSQL_USER'],\
                pw=DB_Config['MYSQL_PASSWD'])


def get_all():
    return db.select('novel_tbl',order='novel_serial Desc')


def get_chapter(novel_serial):
    try:
        return db.select('SELECT chapter_tbl',where ='novel_serial = $novel_serial',vars= locals())
    except Exception as err:
        return None

