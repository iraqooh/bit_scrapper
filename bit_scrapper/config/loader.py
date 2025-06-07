#  Functionality to load and validate the scraper's configuration
import json
import os
from jsonschema import validate, ValidationError

CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "selectors": {
            "type": "object",
            "minProperties": 1
        },
        "pagination": {
            "type": "object",
            "properties": {
                "enabled": {"type": "boolean"},
                "next_selector": {"type": "string"},
                "max_pages": {"type": "integer"}
            },
            "required": ["enabled"]
        }
    },
    "required": ["selectors", "pagination"]
}

def load_config(config_path: str) -> dict:
    """
    Load and return the configuration from a JSON file.

    Args:
        config_path (str): Path to the configuration file.
    
    Returns:
        dict: Parsed configuration data.
    
    Raises:
        FileNotFoundError: If the configuration file does not exist.
        json.JSONDecodeError: If the file content is not a valid JSON.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
        try:
            validate(instance=config, schema=CONFIG_SCHEMA)
        except ValidationError as e:
            raise ValueError(f"Invalid config: {e.message}")
    return config