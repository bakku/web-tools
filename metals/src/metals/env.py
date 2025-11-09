import os


def is_development_mode() -> bool:
    return os.getenv("APP_ENV", "").lower() == "development"
