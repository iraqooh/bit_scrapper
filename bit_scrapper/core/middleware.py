import logging
import random
import time
import requests
from typing import Dict
from requests.exceptions import RequestException, Timeout


class Middleware:
    """
    Basic request middleware for injecting headers, user-agent, delays, and retry handling.

    Args:
        config (dict): Configuration object containing headers, user_agents, delays, and retry settings.
    """

    DEFAULT_USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)",
    ]

    def __init__(self, config: dict) -> None:
        self.config = config
        self.headers = config.get("headers", {})
        self.user_agents = config.get("user_agents", self.DEFAULT_USER_AGENTS)
        self.delay_config = config.get("delay", None)
        self.retry_config = config.get("retry", {})
        self.max_attempts = self.retry_config.get("max_attempts", 3)
        self.backoff_factor = self.retry_config.get("backoff_factor", 0.1)
        self.retry_on_status = self.retry_config.get("retry_on", [500, 502, 503, 504])

    def _get_random_user_agent(self):
        if self.user_agents:
            return random.choice(self.user_agents)
        return "Mozilla/5.0 (compatible)"

    def _apply_random_delay(self) -> None:
        if self.delay_config:
            delay = random.uniform(self.delay_config.get("min", 0), self.delay_config.get("max", 0))
            time.sleep(delay)

    def process_request(self, url: str, headers=None) -> Dict[str, str]:
        """
        Construct and return headers for an outgoing request.

        Args:
            url (str): The target URL (optional use).

        Returns:
            dict: Request headers with randomized user-agent.
        """
        headers = headers or {}
        final_headers = self.headers.copy()
        final_headers.update(headers)
        final_headers["User-Agent"] = self._get_random_user_agent()
        return final_headers

    def fetch_with_retries(self, url: str, headers: Dict[str, str]) -> str:
        """
        Attempt to fetch a URL with retries on timeout or server error.

        Args:
            url (str): The URL to fetch.
            headers (dict): HTTP headers to include in the request.

        Returns:
            str: The response content, or empty string on failure.
        """
        attempt = 0
        while attempt < self.max_attempts:
            try:
                final_headers = self.process_request(url, headers)
                response = requests.get(url, headers=final_headers)
                if response.status_code in self.retry_on_status:
                    # Raise to trigger retry
                    response.raise_for_status()
                elif 400 <= response.status_code < 500:
                    # Client errors: no retry
                    response.raise_for_status()
                    return ""
                else:
                    response.raise_for_status()
                    return response.text
            except (requests.Timeout, requests.ConnectionError):
                # Retry on network issues
                pass
            except requests.HTTPError as e:
                # Retry only on retryable HTTP errors (above)
                if response.status_code not in self.retry_on_status:
                    # Do not retry on non-retryable HTTP errors
                    return ""
            attempt += 1
            # Exponential backoff delay before retry
            time.sleep(self.backoff_factor * (2 ** (attempt - 1)))
        return ""

    def process_response(self, url: str, response: str) -> str:
        """
        Optional hook to modify the HTTP response before returning.

        Args:
            url (str): URL of the request.
            response (str): Raw response text.

        Returns:
            str: (Possibly modified) response text.
        """
        return response
