# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BooksPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.bd = client.books
    
    def process_item(self, item, spider):
        collection = self.bd[spider.name]
        item['authors'] = ' '.join(item['authors'])
        if spider.name == 'labirint':
            item['resource'] = 'labirint.ru'
        else:
            item['resource'] = 'book24.ru'
            
        collection.insert_one(item)
        
        return item
