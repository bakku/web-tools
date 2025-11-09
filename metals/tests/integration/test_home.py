from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from metals.internal.persistency.models import MetalPrice
from metals.internal.types import Metal


def test_loads_home_successfully(client: TestClient, test_db: Session) -> None:
    test_db.add(MetalPrice(metal=Metal.GOLD, price=12.0))
    test_db.add(MetalPrice(metal=Metal.SILVER, price=10.0))
    test_db.commit()

    response = client.get("/")
    content = response.text

    assert response.status_code == 200
    assert "Precious Metals Tracker" in content
    assert "Track your precious metal portfolio" in content
    assert "Gold: 12.00 €" in content
    assert "Silver: 10.00 €" in content
