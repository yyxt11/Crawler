

class CrashDump(object):
    def __init__(self,Redis):
        self.redis = Redis



    def Crashload(self):
        f = open('./Dumpfile/dumpurl.txt', 'r+')
        lines =[]
        for line in f:
            lines.append(line)
        num = len(lines)
        #取倒数前30个url,一页
        if num >=30:
            for i in lines[num-29:]:
                u = i.split('\n')[0]
                self.redis.lpush('NovelCrawler:Novel_url',u)
        elif num == 0:
            return
        else:
            for i in lines:
                u = i.split('\n')[0]
                self.redis.lpush('NovelCrawler:Novel_url', u)

        f.close()

    def CrashPreventlog(self,url):
        try:
            f = open('./Dumpfile/dumpurl.txt', 'a+')
            f.write(url)
            f.write('\n')
            f.close()
        except Exception as err:
            print('===============read error,msg:%s' %err)