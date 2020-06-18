# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import *
import time
import pymysql
from twisted.enterprise import adbapi


class CaipanAreaPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        # 从项目的配置文件中读取相应的参数
        cls.MYSQL_DB_NAME = crawler.settings.get("MYSQL_DBNAME")
        cls.MYSQL_HOST = crawler.settings.get("MYSQL_HOST")
        cls.MYSQL_USER = crawler.settings.get("MYSQL_USER")
        cls.MYSQL_PASSWORD = crawler.settings.get("MYSQL_PASSWORD")
        cls.PORT = crawler.settings.get("PORT")
        cls.TABLE = crawler.settings.get("TABLE")
        return cls()

    def open_spider(self, spider):
        self.dbpool = adbapi.ConnectionPool('pymysql', host=self.MYSQL_HOST, port=self.PORT, user=self.MYSQL_USER,
                                            passwd=self.MYSQL_PASSWORD, db=self.MYSQL_DB_NAME, charset='utf8', use_unicode=True)
    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insert_db, item)
        return item

    def insert_db(self, tx, item):
        if isinstance(item, WenshuScItem):
            field_lists = []
            value_lists = []
            field_num = []
            for k, v in dict(item).items():
                field_lists.append("`"+str(k)+"`")
                value_lists.append(pymysql.escape_string(str(v)))
            [field_num.append('%s') for i in range(1, len(field_lists) + 1)]
            sql = """INSERT IGNORE INTO `{db}`.`{table}` ({fields}) VALUES ({fields_num});""".format(db=self.MYSQL_DB_NAME, table=self.TABLE, fields=','.join(field_lists), fields_num=','.join(field_num))
            try:
                tx.execute(sql, tuple(value_lists))
            except pymysql.InterfaceError:
                self.dbpool = adbapi.ConnectionPool('pymysql', host=self.MYSQL_HOST, port=self.PORT,
                                                    user=self.MYSQL_USER,
                                                    passwd=self.MYSQL_PASSWORD, db=self.MYSQL_DB_NAME, charset='utf8',
                                                    use_unicode=True)
                tx.execute(sql, tuple(value_lists))
            return item
