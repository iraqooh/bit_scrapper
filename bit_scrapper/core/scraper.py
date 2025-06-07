# Implements the core scraping functionality using the Requests library
# BeautifulSoup is used for HTML parsing
# Reads user-defined selectors from the configuration to extract the relevant data
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse, urljoin

from bit_scrapper.utils.logger import setup_logger
from bit_scrapper.utils.cache import load_from_cache, save_to_cache
from bit_scrapper.core.middleware import Middleware

class BitScrapper:
    def __init__(self, config: dict):
        """
        Initialize the scraper with a configuration.

        Args:
            config (dict): Configuration dictionary object containing selectors and pagination options.
        """
        self.config = config
        self.selectors = config.get("selectors", {})
        self.pagination = config.get("pagination", {})
        self.logger = setup_logger()
        self.middleware = Middleware(config)
        self.robot_parser = None
        self.respect_robots = config.get("respect_robots", True)
    
    def _init_robots_txt(self, base_url: str):
        parsed = urlparse(base_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        self.robot_parser = RobotFileParser()
        self.robot_parser.set_url(robots_url)
        try:
            self.robot_parser.read()
            self.logger.info(f"robots.txt loaded from {robots_url}")
        except:
            self.logger.warning(f"Could not read robots.txt at {robots_url}")
    
    def _is_allowed(self, url: str) -> bool:
        if not self.respect_robots:
            return True
        if not self.robot_parser:
            self._init_robots_txt(url)
        return self.robot_parser.can_fetch("*", url)
    
    def fetch_url(self, url: str) -> str:
        """
        Fetches the HTML content from a given URL.

        Args:
            url (str): URL to fetch.
        
        Returns:
            str: HTML content of the web page.
        """
        if not self._is_allowed(url):
            self.logger.warning(f"Blocked by robots.txt: {url}")
            return ""
        
        cached = load_from_cache(url)
        if cached:
            self.logger.info(f"Loaded from cache: {url}")
            return cached
        
        try:
            headers = self.middleware.process_request(url)
            self.logger.info(f"Fetching URL with retry: {url}")
            content = self.middleware.fetch_with_retries(url, headers)
            if content:
                return content
            return ""
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {url} -> {e}")
            return ""
    
    def extract_data(self, html: str) -> dict:
        """
        Extracts the data from the HTML content based on the configured selectors.
        
        Args:
            html (str): HTML content.
        
        Returns:
            dict: Extracted data mapped by selector keys.
        """
        soup = BeautifulSoup(html, 'html.parser')
        extract = {}

        # Iterating through each selector defined in the configuration
        for field, rule in self.selectors.items():
            rule_type = rule.get("type")
            rule_value = rule.get("value")
            # Handling the CSS selectors
            if rule_type == 'css' and rule_value:
                element = soup.select_one(rule_value)
                extract[field] = element.get_text(strip=True) if element else None
            # Stub for XPath selectors
            elif rule_type == 'xpath' and rule_value:
                # placeholder for xpath support
                extract[field] = None
            # Stub for Regex extraction.
            elif rule_type == "regex" and rule_value:
                # For Regex extraction, use the `re` module.
                extract[field] = None
            else:
                extract[field] = None
        return extract
    
    def get_next_page_url(self, soup: BeautifulSoup, current_page: int) -> str:
        if self.pagination.get("strategy") == "link":
            selector = self.pagination.get("next_selector")
            next_link = soup.select_one(selector)
            # return next_link['href'] if next_link and 'href' in next_link.attrs else None
            return urljoin(self.config["start_url"], next_link['href']) if next_link and 'href' in next_link.attrs else None
        elif self.pagination.get("strategy") == "offset":
            base_url = self.pagination.get("base_url")
            offset_param = self.pagination.get("param", "page")
            return f"{base_url}?{offset_param}={current_page+1}"

        return None

    def run(self, start_url: str) -> list:
        """
        The main method that fetches the URL, extracts data, and returns the structured result.
        
        Args:
            url (str): URL to scrape.
        
        Returns:
            dict: Extracted data.
        """
        results = []
        url = start_url
        page = 1
        max_pages = self.pagination.get("max_pages", 1)
        self.config["start_url"] = start_url

        while url and page <= max_pages:
            html = self.fetch_url(url)
            if not html: break
        
            soup = BeautifulSoup(html, 'html.parser')
            data = self.extract_data(html)
            results.append(data)

            # Setup next iteration
            url = self.get_next_page_url(soup, page)
            page += 1
        
        # Later, add retry logic or concurrency

        return results