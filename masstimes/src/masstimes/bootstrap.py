import os
import sys

import dotenv

from masstimes.utils import is_test_env

REQUIRED_ENV_VARS = ["ADMIN_USERNAME", "ADMIN_PASSWORD"]


def _check_env_var(var: str) -> None:
    if os.getenv(var) is None:
        print(f"{var} is not set")
        sys.exit(-1)


def _check_prerequisites() -> None:
    for env_var in REQUIRED_ENV_VARS:
        _check_env_var(env_var)


def bootstrap() -> None:
    """Prepares the application for startup"""
    dotenv.load_dotenv()

    if not is_test_env():
        _check_prerequisites()
