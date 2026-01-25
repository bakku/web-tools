import sys


def is_test_env() -> bool:
    return "pytest" in sys.modules
