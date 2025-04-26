from datetime import datetime
import os


BOT_NAME = "ebay_dailydeals"

SPIDER_MODULES = ["ebay_dailydeals.spiders"]
NEWSPIDER_MODULE = "ebay_dailydeals.spiders"

ROBOTSTXT_OBEY = True

# Pipelines
ITEM_PIPELINES = {
    "ebay_dailydeals.pipelines.CsvExportPipeline": 300,
    "ebay_dailydeals.pipelines.GoogleSheetsPipeline": 400,
}


# Logging
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs("logs", exist_ok=True)
LOG_LEVEL = "INFO"
LOG_FILE = f"logs/scrapy_deals_{timestamp}.log"

# Retry
RETRY_ENABLED = True
RETRY_TIMES = 5

# Export encoding
FEED_EXPORT_ENCODING = "utf-8"

DOWNLOADER_MIDDLEWARES = {
    "ebay_dailydeals.middlewares.ProxyMiddleware": 350,
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 400,
}
