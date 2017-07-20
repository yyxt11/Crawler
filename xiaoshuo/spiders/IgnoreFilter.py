
from xiaoshuo.spiders.Bloomfilter import BloomFilter
import redis



#boolfilter增量，利用redis持久性,1个blocknum == 256MB,可支撑9000万数据去重

class IgnoreItem(object):
    def __init__(self):
        self.host = 'localhost'
        self.port = 6379
        self.db = 0
        self.key = 'NovelCrawler:Ignore'
        self.server = redis.Redis(host=self.host, port=self.port, db=self.db)
        self.bf = BloomFilter(self.server, self.key, blockNum=1)  # you can increase blockNum if your are filtering too many urls

    def filter(self, url):
        if self.bf.isContains(url):
            return False
        else:
            self.bf.insert(url)
            return True

