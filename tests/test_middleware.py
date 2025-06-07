import pytest
import requests
from unittest.mock import patch, MagicMock
from bit_scrapper.core.middleware import Middleware

@pytest.fixture
def config():
    return {
        "user_agents": ["Mozilla/5.0", "Chrome/90.0", "Safari/605.1"],
        "headers": {"X-Custom-Header": "BitScrapper"},
        "delay": {"min": 0.1, "max": 0.3},
        "retry": {
            "max_attempts": 3,
            "backoff_factor": 0.1,
            "retry_on": [500, 502, 503, 504],
        },
    }

def test_user_agent_rotation(config):
    middleware = Middleware(config)
    user_agent = middleware._get_random_user_agent()
    assert user_agent in config["user_agents"]

def test_headers_are_injected(config):
    middleware = Middleware(config)
    final_headers = middleware.process_request("https://example.com")
    assert "User-Agent" in final_headers
    assert final_headers["X-Custom-Header"] == "BitScrapper"

def test_random_delay_within_bounds(config):
    middleware = Middleware(config)
    with patch("time.sleep") as mock_sleep:
        middleware._apply_random_delay()
        called_with = mock_sleep.call_args[0][0]
        # Check against delay config min/max
        assert config["delay"]["min"] <= called_with <= config["delay"]["max"]

def test_no_delay_if_not_configured():
    middleware = Middleware({})
    with patch("time.sleep") as mock_sleep:
        middleware._apply_random_delay()
        mock_sleep.assert_not_called()

def test_retry_on_timeout_and_5xx(config):
    middleware = Middleware(config)

    mock_get = MagicMock()
    mock_get.side_effect = [
        requests.exceptions.Timeout(),
        MagicMock(status_code=500, raise_for_status=MagicMock(side_effect=requests.HTTPError())),
        MagicMock(status_code=200, raise_for_status=MagicMock(return_value=None), text="Success")
    ]

    with patch("requests.get", mock_get):
        content = middleware.fetch_with_retries("https://favqs.com/api", headers={})
        assert content == "Success"
        assert mock_get.call_count == 3

def test_max_retries_exceeded(config):
    config["retry"]["max_attempts"] = 2
    middleware = Middleware(config)

    mock_get = MagicMock()
    mock_get.side_effect = requests.exceptions.Timeout()

    with patch("requests.get", mock_get):
        content = middleware.fetch_with_retries("https://favqs.com/api", headers={})
        assert content == ""
        assert mock_get.call_count == 2

def test_no_retry_on_403_or_404(config):
    middleware = Middleware(config)

    mock_response = MagicMock(
        status_code=404,
        raise_for_status=MagicMock(side_effect=requests.HTTPError("Not Found"))
    )
    mock_get = MagicMock(return_value=mock_response)

    with patch("requests.get", mock_get):
        content = middleware.fetch_with_retries("https://favqs.com/api", headers={})
        assert content == ""
        # Should NOT retry, only 1 call
        assert mock_get.call_count == 1
