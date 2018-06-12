# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from fang.items import NewHouseItem, ESFHouseItem

class FangPipeline(object):
    def __init__(self,host, db):
        self.host = host
        self.db = db

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.host)
        self.table = self.client[self.db]

    def process_item(self, item, spider):
        if isinstance(item, NewHouseItem):
            self.table['new_hose'].insert(dict(item))
        elif isinstance(item, ESFHouseItem):
            self.table['esf_hose'].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = crawler.settings.get('MONDODB_HOST'),
            db = crawler.settings.get('MONDODB_DB')
        )
