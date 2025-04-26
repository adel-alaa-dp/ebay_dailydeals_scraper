from scrapy.crawler import CrawlerProcess
from ebay_dailydeals.spiders.daily_deals_spider import DailyDealsSpider

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(DailyDealsSpider)
    process.start()
