import scrapy
from scrapy.http import HtmlResponse
from jobs.items import JobsItem


class SjruspiderSpider(scrapy.Spider):
    name = 'SjruSpider'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response:HtmlResponse): 
        main_linkSJ = 'https://www.superjob.ru'
        
        nextb = response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()
        links = response.css('a._6AfZ9::attr(href)').extract()
        
        for l in links:            
            yield response.follow(l, callback=self.vacansy_parse)
        if nextb:
            nb = main_linkSJ + nextb
            yield response.follow(nb, callback=self.parse)
            
    def vacansy_parse(self, response:HtmlResponse):
        name = response.css('h1._3mfro::text').extract_first()
        salary = response.xpath("//span[@class='_3mfro _2Wp8I PlM3e _2JVkc']//text()").extract()
        link = response.url
        
        yield JobsItem(name=name, salary=salary, link=link)

        
