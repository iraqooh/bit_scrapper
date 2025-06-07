import pytest
from bit_scrapper.core.scraper import BitScrapper

sample_config = {
    "selectors": {
        "title": {
            "type": "css",
            "value": "h1"
        },
        "summary": {
            "type": "css",
            "value": "p"
        }
    },
    "pagination": {
        "enabled": False
    }
}

sample_html = """
<html>
  <body>
    <h1>Test Title</h1>
    <p>This is a summary.</p>
  </body>
</html>
"""

class MockResponse:
    def __init__(self, text):
        self.text = text
        self.status_code = 200

def mock_fetch(url):
    return sample_html

def test_scraper_extract_data(monkeypatch):
    scraper = BitScrapper(sample_config)
    monkeypatch.setattr(scraper, "fetch_url", lambda url: sample_html)
    result = scraper.run("http://fake-url.com")
    assert isinstance(result, list)
    assert result[0]["title"] == "Test Title"