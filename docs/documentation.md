# BitScrapper

**BitScrapper** is a robust, modular, and highly customizable web scraping framework built using pure Python. It is designed for developers and researchers who need powerful, script-based control over data extraction without relying on GUI-based tools or heavyweight frameworks.

---

## 🚀 Features

- Customizable selectors using **CSS**, **XPath**, or **Regex**
- Supports scraping of static content
- Automatic pagination handling
- Request throttling and random delay configuration
- User-agent rotation
- Exports data to **CSV** or **JSON**
- Configurable retry logic and error logging
- Scheduling via CLI or Python script
- Easily extensible for site-specific parsers or output formats

---

## 🛠️ Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/iraqooh/bit_scrapper.git
cd bit_scrapper
pip install -r requirements.txt
```

---

## 📦 Project Structure

```
bit_scrapper/
├── cli/
│   └── main.py
├── config/
│   └── loader.py
├── core/
│   ├── middleware.py
│   └── scraper.py
├── utils/
│   ├── cache.py
│   ├── logger.py
│   └── writer.py
├── outputs/
├── docs/
├── examples/
│   └── sample_config.json
├── scripts/
│   ├── schedule_scraper.py
│   └── scrape.py
├── tests/
├── .gitignore
├── LICENSE
├── README.md
├── output.json
├── requirements.txt
└── setup.py
```

---

## ⚙️ Configuration

A sample config (`sample_config.json`) may look like:

```json
{
  "selectors": {
    "title": {
      "type": "css",
      "value": "BitScrapper by Iraku Harry"
    },
    "header": {
      "type": "css",
      "value": "h1"
    }
  },
  "pagination": {
    "enabled": true,
    "strategy": "link",
    "next_selector": "a.next",
    "max_pages": 3
  },
  "headers": {
    "User-Agent": "BitScrapperBot/1.0 (+https://github.com/iraqooh/bit_scrapper)"
  },
  "respect_robots": true,
  "user_agents": ["Mozilla/5.0", "Chrome/90.0", "Safari/605.1"],
  "delay": {"min": 0.1, "max": 0.3},
  "retry": {
    "max_attempts": 3,
    "backoff_factor": 0.1,
    "retry_on": [500, 502, 503, 504]
  }
}
```

---

## 🔧 CLI Usage

```bash
python -m bit_scrapper.cli.main --config examples/sample_config.json --url https://target_domain.com --format json --output output
```

---

## ⏰ Scheduling

`scripts/schedule_scraper.py` allows you to schedule runs.

```python
schedule.every().day.at("09:00").do(run_scraper)
```

---

## 📤 Output

- Outputs data to JSON or CSV format.
- Default is `output.json` or `output.csv`.

---

## 📌 Requirements

```
attrs==25.3.0
beautifulsoup4==4.13.4
bs4==0.0.2
certifi==2025.4.26
charset-normalizer==3.4.2
colorama==0.4.6
idna==3.10
iniconfig==2.1.0
jsonschema==4.24.0
jsonschema-specifications==2025.4.1
packaging==25.0
pluggy==1.6.0
Pygments==2.19.1
pytest==8.4.0
referencing==0.36.2
requests==2.32.3
rpds-py==0.25.1
schedule==1.2.2
soupsieve==2.7
typing_extensions==4.14.0
urllib3==2.4.0
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo: [https://github.com/iraqooh/bit_scrapper](https://github.com/iraqooh/bit_scrapper)
2. Create a new branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a Pull Request

Found a bug? Open an issue or suggest a feature.

---

## 📄 License

This project is licensed under the MIT License.

---

**Developed by Iraku Harry**