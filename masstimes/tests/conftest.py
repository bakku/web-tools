from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from masstimes.main import app
from masstimes.routers.admin.app import admin_app
from masstimes.routers.dependencies import get_config
from masstimes.routers.types import AdminConfig, Config


@pytest.fixture
def config() -> Config:
    return Config(admin=AdminConfig(username="test_user", password="test_pass"))


@pytest.fixture
def http_client(config: Config) -> Generator[TestClient, None, None]:
    def override_get_config() -> Generator[Config, None, None]:
        yield config

    app.dependency_overrides[get_config] = override_get_config
    admin_app.dependency_overrides[get_config] = override_get_config

    yield TestClient(app)

    app.dependency_overrides.clear()
    admin_app.dependency_overrides.clear()
