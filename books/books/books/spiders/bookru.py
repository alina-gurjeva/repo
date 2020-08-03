import scrapy
from scrapy.http import HtmlResponse
from books.items import BooksItem


class BookruSpider(scrapy.Spider):
    name = 'bookru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=комиксы'] #ищем комиксы
    

    def parse(self, response):
        nextb = response.xpath("//a[6]/@href").extract_first()
        links = response.xpath("//a[contains(@class,'book__title-link')]/@href").extract()
        
        for l in links:
            yield response.follow(l, callback = self.books_parse)
            
        if nextb:
            yield response.follow(nextb, callback = self.parse)
            
    def books_parse(self, response):
        # Ссылка на книку
        link = response.url
        # Наименование книги
        name = response.xpath("//h1[@class='item-detail__title']//text()").extract_first()
        # Автор(ы)
        authors = response.xpath('//div[1][@class="item-tab__chars-item"]//a//text()').extract() #может быть не 1 автор
        # Основную цену
        price = response.xpath("//div[@class='item-actions__price-old']//text()").extract_first()
        # Цену со скидкой
        discount_price = response.xpath("//div[@class='item-actions__prices']//b//text()").extract_first()
        # Рейтинг книги
        raiting = response.xpath("//span[@class='rating__rate-value']//text()").extract_first()
        
        if not price:
            price = discount_price
        
        yield BooksItem(link=link, name=name, authors=authors, price=price, discount_price=discount_price,
                        raiting=raiting)        
