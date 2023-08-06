import threading
import time
import pymysql


# 每隔两分钟检查一次redis，若没有新的数据插入，则终止爬虫
class MonitorRedis(threading.Thread):
    def __init__(self, redis, spider, redis_key):
        threading.Thread.__init__(self)
        self.redis = redis
        self.spider = spider
        self.redis_key = redis_key

    def run(self):
        while True:
            start_nums = self.redis.scard(self.redis_key)
            time.sleep(2 * 60)
            end_nums = self.redis.scard(self.redis_key)
            if end_nums == start_nums:
                self.spider.crawler.engine.close_spider(self.spider, 'Data Collection And Completion')
                break


# 每隔五分钟检查一次Mysql是否有新的数据插入，若没有则关闭爬虫
class MonitorMysql(threading.Thread):
    def __init__(self, db, cursor, spider, table):
        threading.Thread.__init__(self)
        self.db = db
        self.cursor = cursor
        self.spider = spider
        self.table = table

    def run(self):
        while True:
            sql = 'select count(*) from %s' % self.table
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
            start_nums = self.cursor.fetchone()[0]
            time.sleep(5 * 60)
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
            stop_nums = self.cursor.fetchone()[0]
            if stop_nums == start_nums:
                self.spider.crawler.engine.close_spider(self.spider, 'Data Collection And Completion')
                break