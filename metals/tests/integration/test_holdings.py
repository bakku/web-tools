import uuid

from bs4 import BeautifulSoup
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from metals.internal.persistency.models import Holding, MetalPrice, Portfolio
from metals.internal.types import Metal


def test_holdings_new_renders_successfully(
    client: TestClient, test_session: Session
) -> None:
    portfolio_id = uuid.uuid4()

    test_session.add(MetalPrice(metal=Metal.GOLD, price=12.0))
    test_session.add(MetalPrice(metal=Metal.SILVER, price=10.0))
    test_session.add(Portfolio(id=portfolio_id))
    test_session.commit()

    response = client.get(f"/p/{portfolio_id}/holdings/new")

    assert response.status_code == 200
    assert "Add Holding" in response.text


def test_holdings_create_inserts_a_holding_successfully(
    client: TestClient, test_session: Session
) -> None:
    portfolio_id = uuid.uuid4()

    test_session.add(Portfolio(id=portfolio_id))
    test_session.commit()

    response = client.post(
        f"/p/{portfolio_id}/holdings",
        data={
            "description": "Krugerrand",
            "metal": "Gold",
            "quantity": "5.0",
            "purchase_price": "8.0",
        },
        follow_redirects=False,
    )

    holdings = test_session.scalars(select(Holding)).all()

    assert response.status_code == 303
    assert response.headers["Location"] == f"/p/{portfolio_id}"
    assert len(holdings) == 1
    assert holdings[0].description == "Krugerrand"
    assert holdings[0].metal == Metal.GOLD
    assert holdings[0].quantity == 5.0
    assert holdings[0].purchase_price == 8.0


def test_holdings_create_redirects_to_portfolio_show(
    client: TestClient, test_session: Session
) -> None:
    portfolio_id = uuid.uuid4()

    test_session.add(MetalPrice(metal=Metal.GOLD, price=12.0))
    test_session.add(MetalPrice(metal=Metal.SILVER, price=10.0))
    test_session.add(Portfolio(id=portfolio_id))
    test_session.commit()

    response = client.post(
        f"/p/{portfolio_id}/holdings",
        data={
            "description": "Krugerrand",
            "metal": "Gold",
            "quantity": "5.0",
            "purchase_price": "8.0",
        },
    )

    assert response.status_code == 200
    assert "Your portfolio" in response.text
    assert "Krugerrand" in response.text


def test_holdings_edit_renders_successfully(
    client: TestClient, test_session: Session
) -> None:
    portfolio_id = uuid.uuid4()
    holding_id = uuid.uuid4()

    test_session.add(MetalPrice(metal=Metal.GOLD, price=12.0))
    test_session.add(MetalPrice(metal=Metal.SILVER, price=10.0))
    test_session.add(
        Portfolio(
            id=portfolio_id,
            holdings=[
                Holding(
                    id=holding_id,
                    description="Britannia",
                    metal=Metal.GOLD,
                    quantity=2.0,
                    purchase_price=6.0,
                )
            ],
        )
    )
    test_session.commit()

    response = client.get(f"/p/{portfolio_id}/holdings/{holding_id}/edit")

    soup = BeautifulSoup(response.text, "html.parser")

    assert response.status_code == 200
    assert "Edit Holding" in response.text

    description_input = soup.find("input", {"name": "description"})
    assert description_input is not None
    assert description_input["value"] == "Britannia"

    quantity_input = soup.find("input", {"name": "quantity"})
    assert quantity_input is not None
    assert quantity_input["value"] == "2.0"

    purchase_price_input = soup.find("input", {"name": "purchase_price"})
    assert purchase_price_input is not None
    assert purchase_price_input["value"] == "6.0"


def test_holdings_update_modifies_holding_successfully(
    client: TestClient, test_session: Session
) -> None:
    portfolio_id = uuid.uuid4()
    holding_id = uuid.uuid4()

    test_session.add(
        Portfolio(
            id=portfolio_id,
            holdings=[
                Holding(
                    id=holding_id,
                    description="Britannia",
                    metal=Metal.GOLD,
                    quantity=2.0,
                    purchase_price=6.0,
                )
            ],
        )
    )
    test_session.commit()

    response = client.post(
        f"/p/{portfolio_id}/holdings/{holding_id}",
        data={
            "description": "Updated Britannia",
            "metal": "Silver",
            "quantity": "3.0",
            "purchase_price": "7.0",
        },
        follow_redirects=False,
    )

    test_session.expire_all()
    holding = test_session.get(Holding, holding_id)

    assert response.status_code == 303
    assert response.headers["Location"] == f"/p/{portfolio_id}"
    assert holding is not None
    assert holding.description == "Updated Britannia"
    assert holding.metal == Metal.SILVER
    assert holding.quantity == 3.0
    assert holding.purchase_price == 7.0


def test_holdings_update_redirects_to_portfolio_show(
    client: TestClient, test_session: Session
) -> None:
    portfolio_id = uuid.uuid4()
    holding_id = uuid.uuid4()

    test_session.add(MetalPrice(metal=Metal.GOLD, price=12.0))
    test_session.add(MetalPrice(metal=Metal.SILVER, price=10.0))
    test_session.add(
        Portfolio(
            id=portfolio_id,
            holdings=[
                Holding(
                    id=holding_id,
                    description="Britannia",
                    metal=Metal.GOLD,
                    quantity=2.0,
                    purchase_price=6.0,
                )
            ],
        )
    )
    test_session.commit()

    response = client.post(
        f"/p/{portfolio_id}/holdings/{holding_id}",
        data={
            "description": "Updated Britannia",
            "metal": "Silver",
            "quantity": "3.0",
            "purchase_price": "7.0",
        },
    )

    assert response.status_code == 200
    assert "Your portfolio" in response.text
    assert "Updated Britannia" in response.text


def test_holdings_delete_removes_holding_successfully(
    client: TestClient, test_session: Session
) -> None:
    portfolio_id = uuid.uuid4()
    holding_id = uuid.uuid4()

    test_session.add(
        Portfolio(
            id=portfolio_id,
            holdings=[
                Holding(
                    id=holding_id,
                    description="Britannia",
                    metal=Metal.GOLD,
                    quantity=2.0,
                    purchase_price=6.0,
                )
            ],
        )
    )
    test_session.commit()

    response = client.post(
        f"/p/{portfolio_id}/holdings/{holding_id}/delete", follow_redirects=False
    )

    holdings = test_session.scalars(select(Holding)).all()

    assert response.status_code == 303
    assert response.headers["Location"] == f"/p/{portfolio_id}"
    assert len(holdings) == 0


def test_holdings_delete_redirects_to_portfolio_show(
    client: TestClient, test_session: Session
) -> None:
    portfolio_id = uuid.uuid4()
    holding_id = uuid.uuid4()

    test_session.add(MetalPrice(metal=Metal.GOLD, price=12.0))
    test_session.add(MetalPrice(metal=Metal.SILVER, price=10.0))
    test_session.add(
        Portfolio(
            id=portfolio_id,
            holdings=[
                Holding(
                    id=holding_id,
                    description="Britannia",
                    metal=Metal.GOLD,
                    quantity=2.0,
                    purchase_price=6.0,
                )
            ],
        )
    )
    test_session.commit()

    response = client.post(f"/p/{portfolio_id}/holdings/{holding_id}/delete")

    assert response.status_code == 200
    assert "Your portfolio" in response.text
    assert "No holdings yet" in response.text
