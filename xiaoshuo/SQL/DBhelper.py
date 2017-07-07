import pymysql

from xiaoshuo.SQL.setting import DB_Config


class dBhelper():
    def __init__(self):
        host = DB_Config['MYSQL_HOST']
        db = DB_Config['MYSQL_DBNAME']
        password = DB_Config['MYSQL_PASSWD']
        user = DB_Config['MYSQL_USER']
        self.connect = pymysql.connect(host, user, password, db, charset='utf8', use_unicode=True)
        self.cursor = self.connect.cursor()


    #捕获插入
    def insert_novel(self, xs_name,xs_author,xs_category,xs_serial):

        try:
            self.cursor.execute("""insert into novel_tbl(novel_name,novel_author,category,novel_serial)
                                value(%s,%s,%s,%s)""",
                                (xs_name, xs_author, xs_category, xs_serial))
            self.connect.commit()
        except Exception as err:
            print(err)

    #去重
    def select_novel(self, xs_name):

        try:
            self.cursor.execute("""select*from novel_tbl where novel_name = %s""", xs_name)
            ret = self.cursor.fetchone()
            if ret:
                return True
            else:
                return False

        except Exception as err:
            print(err)

    #捕获插入
    def insert_chapter(self, chapter_name,chapter_content,novel_serialnum,sectionnum,chapter_url):
        try:
            self.cursor.execute("""insert into chapter_tbl(chapter_name,chapter_content,sectionnum,chapter_url,novel_serial)
                                value(%s,%s,%s,%s,%s)""",
                                (chapter_name,chapter_content,sectionnum,chapter_url,novel_serialnum))
            self.connect.commit()
        except Exception as err:
            print(err)


    #去重
    def select_chapter(self, chapter_url):

        try:
            self.cursor.execute("""select*from chapter_tbl where chapter_url = %s""", chapter_url)
            ret = self.cursor.fetchone()
            if ret:
                return True
            else:
                return False

        except Exception as err:
            print(err)




# 测试
if __name__ == '__main__':
    db = dBhelper()
    pass



