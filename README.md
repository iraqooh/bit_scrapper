# BitScrapper 🕷️
**BitScrapper** is a robust, modular, and highly customizable web scraping framework built using pure Python. Designed for developers and researchers who need powerful, script-based control over data extraction without relying on GUI-based tools or heavyweight frameworks.

---

## 📦 Features

- 🔍 Customizable selectors using **CSS**, **XPath**, or **Regex**
- ⚙️ Supports scraping of static content
- 🔄 Automatic pagination handling
- 🕰️ Request throttling and random delay configuration
- 🌐 User-agent rotation
- 🗃️ Exports data to **CSV** or **JSON**.
- 🛠️ Configurable retry logic and error logging
- 🗓️ Scheduling via CLI or Python script
- 🧩 Easily extensible for site-specific parsers or output formats

---

## 🏗️ Project Structure
```bash
BitSkrapper/
├── bitskrapper/
│ ├── init.py
│ ├── core/ # Core scraping logic
│ ├── selectors/ # Selector modules
│ ├── outputs/ # Exporters for JSON, CSV, DB
│ ├── middleware/ # Throttling, retry, logging, etc.
│ ├── scheduler/ # CLI job scheduler
│ └── config/ # Config templates and parser
├── examples/ # Example config files and scripts
├── tests/ # Unit and integration tests
├── scripts/ # CLI entry points
├── README.md
├── requirements.txt
└── setup.py
```

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.8+
- pip or pipenv
- [Playwright](https://playwright.dev/python/) or [Selenium](https://www.selenium.dev/) (optional for dynamic content)

### 📥 Installation

```bash
git clone https://github.com/iraqooh/bit_scrapper.git
cd BitSkrapper
pip install -r requirements.txt
# For dynamic scraping (optional)
playwright install
```

🕹️ Usage

⚙️ Basic Scrape Example

```bash
python scripts/scrape.py --url "https://target_domain.com" --config "examples/products.json"
```

📁 Batch Mode with CSV Input

```bash
python scripts/scrape.py --input-file "input/urls.csv" --config "examples/article_config.json"
```

🗃️ Output Options

```bash
# Save to CSV
--format csv --output "output/results.csv"
# Save to MongoDB
--format mongo --mongo-uri "mongodb://localhost:27017" --db "scrapes" --collection "products"
```

🛡️ Auth & Headers

```bash
--headers '{"Authorization": "Bearer <TOKEN>", "User-Agent": "BitSkrapper/1.0"}'
--cookies "sessionid=abcd1234"
```

🔄 Scheduling Scraping Jobs

Use the CLI-based scheduler:

```bash
python scripts/schedule.py --task "examples/daily_scrape.json"
```

🔧 Configuration

BitScrapper uses JSON/YAML config files to define scraping behavior.

Sample Config (products.json)

```json
{
  "selectors": {
    "title": ".product-title",
    "price": ".price",
    "link": {"type": "attribute", "selector": ".product a", "attr": "href"}
  },
  "pagination": {
    "next_button": ".pagination-next",
    "max_pages": 10
  },
  "headers": {
    "User-Agent": "BitSkrapperBot/1.0"
  },
  "delay_range": [1, 3],
  "output": {
    "format": "csv",
    "path": "output/products.csv"
  }
}
```


🧪 Testing & Validation

```bash
pytest tests/
```

To preview selectors:

```bash
python scripts/test_selector.py --url "https://example.com" --selector ".item-title"
```

📚 Documentation

Comprehensive docs and usage examples are available in the /docs directory.

🤝 Contributing

Contributions are welcome! Please fork the repo and submit a pull request. Open an issue for bugs or feature requests.

🛡️ License

GNU General Public License v3

🧠 Credits

Created with passion by Mr. Iraku. Inspired by Scrapy, Playwright, and other great scraping tools, but keeping it Pythonic and minimal.

🔗 Related Tools

requests

BeautifulSoup

lxml

playwright-python

fake_useragent

pymongo
