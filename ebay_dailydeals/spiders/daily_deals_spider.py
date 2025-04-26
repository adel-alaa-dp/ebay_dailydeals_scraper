import scrapy
import json
import math
import re
from datetime import datetime
from scrapy.http import Request
from ebay_dailydeals.items import EbayDailyDealItem


class DailyDealsSpider(scrapy.Spider):
    name = "daily_deals"
    allowed_domains = ["ebay.com"]
    start_urls = ["https://www.ebay.com/globaldeals"]

    custom_settings = {"LOG_FILE": "logs/scrapy_deals.log"}

    def parse(self, response):
        links = response.xpath('//*[@class="dne-show-more-link"]/a/@href').extract()
        for link in links:
            path = re.findall(r'https:\/\/www\.ebay\.com\/globaldeals\/([^"\n]+)', link)
            if not path:
                continue
            segment = path[0]
            if segment.startswith("featured/"):
                segment = segment.replace("featured/", "").replace(
                    "/all", "&deal_type=featured"
                )
            else:
                segment = segment.replace("/", ",")
            yield from self.scrape_category(segment)

    def scrape_category(self, category_path):
        timestamp = int(datetime.now().timestamp() * 1000)
        url = f"https://www.ebay.com/globaldeals/spoke/ajax/listings?t={timestamp}&_ofs=0&category_path_seo={category_path}"
        yield Request(
            url,
            callback=self.parse_listing_page,
            meta={"category_path": category_path, "page": 0},
        )

    def parse_listing_page(self, response):
        data = json.loads(response.text)
        status = (
            data.get("fulfillmentValue", {})
            .get("pagination", {})
            .get("text", {})
            .get("status", "")
        )
        total_results = int(re.findall(r"(\d+)", status)[-1]) if status else 0
        listings_html = data.get("fulfillmentValue", {}).get("listingsHtml", "")

        if listings_html:
            yield from self.parse_products(listings_html)

        current_page = response.meta["page"]
        category_path = response.meta["category_path"]
        total_pages = math.ceil(total_results / 24)

        if current_page + 1 < total_pages:
            next_offset = (current_page + 1) * 24
            timestamp = int(datetime.now().timestamp() * 1000)
            next_url = f"https://www.ebay.com/globaldeals/spoke/ajax/listings?t={timestamp}&_ofs={next_offset}&category_path_seo={category_path}"
            yield Request(
                next_url,
                callback=self.parse_listing_page,
                meta={"category_path": category_path, "page": current_page + 1},
            )

    def parse_products(self, html_source):
        tree = scrapy.Selector(text=html_source)
        products = tree.xpath('//*[@class="item-grid-spoke"]//*[@class="col"]')
        for product in products:
            item = EbayDailyDealItem()
            item["title"] = product.xpath('.//*[@itemprop="name"]/text()').get()
            item["price"] = (
                product.xpath('.//*[@itemprop="price"]/text()')
                .get(default="")
                .replace("US $", "")
            )
            item["url"] = product.xpath("./a/@href").get()
            item["image"] = product.xpath(".//img/@src").get()
            item["sku"] = (
                re.findall(r"/itm/(\d+)?", item["url"] or "")[0]
                if item["url"]
                else None
            )
            item["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            yield item
