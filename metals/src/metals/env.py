import os


def is_development_mode() -> bool:
    """
    Check if the application is running in development mode.

    Returns:
        True if APP_ENV environment variable is set to "development", False otherwise.
    """
    return os.getenv("APP_ENV", "").lower() == "development"
