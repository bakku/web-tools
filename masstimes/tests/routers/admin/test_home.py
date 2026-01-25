import httpx
from fastapi import status
from fastapi.testclient import TestClient

from masstimes.routers.types import Config


def test_home_should_return_unauthorized_if_credentials_incorrect(
    http_client: TestClient,
) -> None:
    response = http_client.get(
        "/admin", auth=httpx.BasicAuth(username="invalid", password="invalid")
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_home_should_load_successfully(http_client: TestClient, config: Config) -> None:
    response = http_client.get(
        "/admin",
        auth=httpx.BasicAuth(
            username=config.admin.username, password=config.admin.password
        ),
    )

    assert response.status_code == status.HTTP_200_OK
