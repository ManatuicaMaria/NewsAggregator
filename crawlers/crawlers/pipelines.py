# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
sys.path.insert(0,'..')
sys.path.insert(0,'../..')
sys.path.insert(0,'../../..')

from esutils import elastic_search as es


class CrawlersPipeline(object):

    def open_spider(self, spider):
        self.json_array = []

    def close_spider(self, spider):
        es.index_bulk(self.json_array)

    def process_item(self, item, spider):
        json_obj = dict(item)
        self.json_array.append(json_obj)
        return item
