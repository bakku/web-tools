from fastapi import status
from fastapi.testclient import TestClient


def test_home_should_load_successfully(http_client: TestClient) -> None:
    response = http_client.get("/")
    assert response.status_code == status.HTTP_200_OK
