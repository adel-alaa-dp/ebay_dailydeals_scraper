import scrapy


class EbayDailyDealItem(scrapy.Item):
    sku = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    date = scrapy.Field()
