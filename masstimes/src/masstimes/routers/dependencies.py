import os

from masstimes.routers.types import AdminConfig, Config


def get_config() -> Config:
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    assert admin_username is not None
    assert admin_password is not None

    return Config(admin=AdminConfig(username=admin_username, password=admin_password))
