import scrapy
from scrapy.http import HtmlResponse
from books.items import BooksItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%9A%D0%BE%D0%BC%D0%B8%D0%BA%D1%81%D1%8B/?stype=0'] #ищем комиксы

    def parse(self, response):
        nextb = response.xpath('//div[@class="pagination-next pagination-next-mobile"]/a[@class="pagination-next__text"]/@href').extract_first()
        links = response.xpath('//div[@class="products-row "]//a[@class="product-title-link"]/@href').extract()
        
        for l in links:
            yield response.follow(l, callback=self.books_parse)
            
        if nextb:
            yield response.follow(nextb, callback = self.parse)
            
    def books_parse(self, response):
        # Ссылка на книку
        link = response.url
        # Наименование книги
        name = response.xpath('//div[@id="product-title"]/h1//text()').extract_first()
        # Автор(ы)
        authors = response.xpath('//div[@class="authors"][1]//text()').extract() #может быть не 1 автор
        # Основную цену
        price = response.xpath("//span[@class='buying-priceold-val-number']//text()").extract_first()
        # Цену со скидкой
        discount_price = response.xpath("//span[@class='buying-pricenew-val-number']//text()").extract_first()
        # Рейтинг книги
        raiting = response.xpath("//div[@id='rate']//text()").extract_first()
        
        yield BooksItem(link=link, name=name, authors=authors, price=price, discount_price=discount_price,
                        raiting=raiting)
