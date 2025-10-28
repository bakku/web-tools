from fastapi.testclient import TestClient

from metals.main import app

client = TestClient(app)


def test_loads_home_successfully() -> None:
    response = client.get("/")
    content = response.text

    assert response.status_code == 200
    assert "Precious Metals Tracker" in content
    assert "Track your precious metal portfolio" in content
