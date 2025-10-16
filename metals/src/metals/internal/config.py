"""Configuration management for the metals application."""

import os


def get_gold_api_key() -> str:
    """
    Get the Gold API key from environment variables.
    
    Returns:
        The API key for gold-api.com
        
    Raises:
        ValueError: If the API key is not configured
    """
    api_key = os.environ.get("GOLD_API_KEY")
    if not api_key:
        raise ValueError(
            "GOLD_API_KEY environment variable is not set. "
            "Please obtain an API key from https://www.gold-api.com/ "
            "and set it in the environment."
        )
    return api_key
