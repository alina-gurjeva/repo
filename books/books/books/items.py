# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field() 
    # Ссылку на книгу
    link = scrapy.Field()
    # Наименование книги
    name = scrapy.Field()
    # Автор(ы)
    authors = scrapy.Field()
    # Основную цену
    price = scrapy.Field()
    # Цену со скидкой
    discount_price = scrapy.Field()
    # Рейтинг книги
    raiting = scrapy.Field()
    #откуда
    resource = scrapy.Field()
    pass
