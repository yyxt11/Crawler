from scrapy import cmdline
import time
cmdline.execute('scrapy crawl Novel_master -s JOBDIR=crawls/Novel_master-1'.split())
#time.sleep(1)
