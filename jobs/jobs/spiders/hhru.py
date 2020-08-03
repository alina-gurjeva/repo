import scrapy
from scrapy.http import HtmlResponse
from jobs.items import JobsItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&fromSearch=true&text=python']
    

    def parse(self, response: HtmlResponse):
        
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
              
        vacansy = response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        
        for link in vacansy:
            yield response.follow(link, callback=self.vacancy_parse)
            
        if next_page:
            yield response.follow(next_page, callback=self.parse)
            
            
    def vacancy_parse(self, response: HtmlResponse):
        
        name = response.xpath("//div[@class='vacancy-title']//text()").extract_first()
        salary = response.xpath("//p[@class='vacancy-salary']/span//text()").extract()
        link = response.url
        
        yield JobsItem(name=name, salary=salary, link=link)
        
        
        
        
