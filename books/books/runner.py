from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from books import settings
from books.spiders.bookru import BookruSpider
from books.spiders.labirint import LabirintSpider

if __name__ == '__main__':
    crawling_settings = Settings()
    crawling_settings.setmodule(settings)
    
    Process = CrawlerProcess(settings = crawling_settings)
    Process.crawl(BookruSpider)
    Process.crawl(LabirintSpider)
    Process.start()