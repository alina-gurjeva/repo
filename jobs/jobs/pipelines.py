# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobsPipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.vacansy    
    

    
    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        if spider.name == 'hhru':
            item['source'] = 'hh.ru'
        else:
            item['source'] = 'superjob.ru'

        salary = item['salary']
        item['min_salary'],item['max_salary'],item['cur'] = self.process_salary(salary)
        
        collection.insert_one(item)
        return item

    
    def process_salary(self, salary):
        
        import re 
        pattern = re.compile('\d')
        
        text = ' '.join(salary) 
        
        if 'налогов' in text:
            text = text[:-18]
        
        if 'договорённости' in text or 'указана' in text:
            frSJ = 0
            toSJ = 0
            currencySJ = 0
        elif '—' in text or ('от' in text and 'до' in text):
            if '—' in text:
                a, b = text.split('—')
            elif ('от' in text and 'до' in text):
                a, b = text.split('до')
            a = int(''.join(pattern.findall(a)))
            b = int(''.join(pattern.findall(b)))
            frSJ = a
            toSJ = b
            x = len(text)
            if 'руки'in text:
                text = text[:-7]
            currencySJ = text[x-4:-1]            
        

        elif 'от' in text:
            a = int(''.join(pattern.findall(text)))
            frSJ = a
            toSJ = 0
            x = len(text)
            if 'руки'in text:
                text = text[:-7]
            currencySJ = text[x-4:-1]           
        elif 'до' in text:
            b = int(''.join(pattern.findall(text)))
            frSJ = 0
            toSJ = b
            x = len(text)
            if 'руки'in text:
                text = text[:-7]
            currencySJ = text[x-4:-1]
        else:
            s = int(''.join(pattern.findall(text)))
            frSJ = s
            toSJ = s
            x = len(text)
            if 'руки'in text:
                text = text[:-7]
            currencySJ = text[x-4:-1]       

        min_salary,max_salary,cur = frSJ,toSJ,currencySJ
        return min_salary,max_salary,cur