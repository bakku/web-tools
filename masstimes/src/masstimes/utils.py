import os
import sys


def is_test_env() -> bool:
    return "pytest" in sys.modules


def is_development_env() -> bool:
    return os.getenv("APP_ENV", "development").lower() == "development"
