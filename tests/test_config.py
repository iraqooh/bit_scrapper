import pytest
from bit_scrapper.config.loader import load_config

def test_valid_config_loads():
    config = load_config("examples/sample_config.json")
    assert "selectors" in config
    assert isinstance(config["selectors"], dict)

def test_invalid_path():
    with pytest.raises(FileNotFoundError):
        load_config("invalid/path/config.json")