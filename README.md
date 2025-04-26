# 📦 eBay Daily Deals Scraper (Scrapy Project)

A professional-grade Scrapy spider that scrapes the latest daily deals from [eBay Global Deals](https://www.ebay.com/globaldeals), exporting data to:

- 📂 Local CSV file (`exports/` folder)
- 📄 Google Sheets (optional)

---

## 🚀 Features

- Scrapes all daily deal categories
- Handles AJAX paginated content
- Supports retries with exponential backoff
- Exports to both CSV and Google Sheets
- Logs all activities to `logs/`
- Duplicate product detection (SKU-based)
- Professional project structure

---

## 🛠 Installation

```bash
# Clone the repository
$ git clone https://github.com/your_username/ebay_dailydeals_scraper.git
$ cd ebay_dailydeals_scraper

# Install dependencies
$ pip install -r requirements.txt
```

Dependencies:
- `scrapy`
- `gspread`
- `oauth2client`
- `lxml`

```bash
pip install scrapy gspread oauth2client lxml
```

---

## ⚙️ Project Structure

```
.
├── ebay_dailydeals/
│   ├── items.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders/
│       └── daily_deals_spider.py
├── exports/
├── logs/
├── requirements.txt
├── run_spider.py
├── scrapy.cfg  
└── README.md

```

---

## 📋 Usage

```bash
python run_spider.py
```

After crawling:
- CSV is saved in `exports/`
- Google Sheet is updated if credentials are configured

> **Note:** To enable Google Sheets export, place your service account JSON file in the root directory and update its filename in `pipelines.py`.
> **Note:** Place our proxy in `middlewares.py`.

---

## 🧹 To-Do
- [ ] Add Dockerfile for containerization
- [ ] Add GitHub Actions CI/CD workflow
- [ ] Extend spider to handle different regions (UK, DE, etc.)

---

## 🧑‍💻 Author

- Built by [Adel Alaa](https://github.com/adel-alaa-dp)
- Linkedin: https://www.linkedin.com/in/adel-alaa/
