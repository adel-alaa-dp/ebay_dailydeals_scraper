import csv
import os
import time
import logging
from datetime import datetime
from scrapy.exceptions import DropItem


class CsvExportPipeline:
    def open_spider(self, spider):
        os.makedirs("exports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"exports/deals_{timestamp}.csv"
        self.file = open(self.filename, mode="w", newline="", encoding="utf-8")
        self.writer = csv.DictWriter(
            self.file, fieldnames=["sku", "title", "price", "url", "image", "date"]
        )
        self.writer.writeheader()
        self.seen = set()

    def process_item(self, item, spider):
        if item["sku"] in self.seen:
            raise DropItem(f"Duplicate item found: {item['sku']}")
        self.seen.add(item["sku"])
        self.writer.writerow(item)
        return item

    def close_spider(self, spider):
        self.file.close()


class GoogleSheetsPipeline:
    def __init__(self):
        try:
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials

            self.gspread = gspread
            self.ServiceAccountCredentials = ServiceAccountCredentials
        except ImportError:
            raise DropItem("Google Sheets libraries not installed.")

    def open_spider(self, spider):
        creds_file = ""  # Update with your credentials file path
        if not os.path.exists(creds_file):
            raise DropItem("Google credentials file not found.")

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = self.ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        client = self.gspread.authorize(creds)
        self.sheet = client.open("").sheet1  # Update with your Google Sheet name

        self.EXPECTED_HEADER = ["SKU", "Title", "Price", "URL", "Image", "date"]
        existing_header = self.sheet.row_values(1)
        if existing_header != self.EXPECTED_HEADER:
            self.sheet.update(range_name="A1:F1", values=[self.EXPECTED_HEADER])

        self.sheet.resize(cols=len(self.EXPECTED_HEADER))
        existing_data = self.sheet.get_all_records()
        self.existing_skus = {
            row["SKU"]: idx + 2 for idx, row in enumerate(existing_data)
        }
        self.to_append = []

    def process_item(self, item, spider):
        row = [
            item["sku"],
            item["title"],
            item["price"],
            item["url"],
            item["image"],
            item["date"],
        ]
        if item["sku"] in self.existing_skus:
            row_index = self.existing_skus[item["sku"]]
            self.sheet.update(f"A{row_index}:F{row_index}", [row])
        else:
            self.to_append.append(row)
        return item

    def close_spider(self, spider):
        for i in range(5):
            try:
                if self.to_append:
                    self.sheet.append_rows(self.to_append)
                break
            except Exception as e:
                wait = 2**i
                logging.warning(f"Google Sheets API quota hit. Retrying in {wait}s...")
                time.sleep(wait)
