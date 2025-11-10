import re
import uuid

from bs4 import BeautifulSoup
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from metals.internal.persistency.models import Holding, MetalPrice, Portfolio
from metals.internal.types import Metal


def test_portfolios_create_inserts_a_portfolio_successfully(
    client: TestClient, test_session: Session
) -> None:
    response = client.post("/p/", follow_redirects=False)

    portfolios = test_session.scalars(select(Portfolio)).all()

    assert response.status_code == 303
    assert response.headers["Location"] is not None
    assert len(portfolios) == 1
    assert portfolios[0].id == uuid.UUID(response.headers["Location"].split("/")[-1])


def test_portfolios_create_redirects_to_portfolio_show(
    client: TestClient, test_session: Session
) -> None:
    test_session.add(MetalPrice(metal=Metal.GOLD, price=12.0))
    test_session.add(MetalPrice(metal=Metal.SILVER, price=10.0))
    test_session.commit()

    response = client.post("/p/")

    assert response.status_code == 200
    assert "Your portfolio" in response.text


def test_portfolios_show_renders_successfully_with_no_holdings(
    client: TestClient, test_session: Session
) -> None:
    portfolio_id = uuid.uuid4()

    test_session.add(MetalPrice(metal=Metal.GOLD, price=12.0))
    test_session.add(MetalPrice(metal=Metal.SILVER, price=10.0))
    test_session.add(Portfolio(id=portfolio_id))
    test_session.commit()

    response = client.get(f"/p/{portfolio_id}")

    assert response.status_code == 200
    assert "Your portfolio" in response.text
    assert "No holdings yet" in response.text
    assert "Gold: 12.00 €" in response.text
    assert "Silver: 10.00 €" in response.text


def test_portfolios_show_renders_portfolio_table(
    client: TestClient, test_session: Session
) -> None:
    portfolio_id = uuid.uuid4()
    holding_one_id = uuid.uuid4()
    holding_two_id = uuid.uuid4()

    test_session.add_all(
        [
            MetalPrice(metal=Metal.GOLD, price=12.0),
            MetalPrice(metal=Metal.SILVER, price=10.0),
            Portfolio(
                id=portfolio_id,
                holdings=[
                    Holding(
                        id=holding_one_id,
                        description="Britannia",
                        metal=Metal.GOLD,
                        quantity=2,
                        purchase_price=6.0,
                    ),
                    Holding(
                        id=holding_two_id,
                        description="Maple Leaf",
                        metal=Metal.SILVER,
                        quantity=3,
                        purchase_price=5.0,
                    ),
                ],
            ),
        ]
    )
    test_session.commit()

    response = client.get(f"/p/{portfolio_id}")

    soup = BeautifulSoup(response.text, "html.parser")

    assert response.status_code == 200

    table_body = soup.tbody

    assert table_body is not None

    table_rows = table_body("tr")

    assert len(table_rows) == 2

    first_row_cells = table_rows[0]("td")

    assert len(first_row_cells) == 7

    first_holding_link = first_row_cells[0].a

    assert first_holding_link is not None
    assert str(first_holding_link["href"]).endswith(
        f"/p/{portfolio_id}/holdings/{holding_one_id}/edit"
    )
    assert first_row_cells[0].text == "Britannia"

    assert first_row_cells[1].text == "Gold"
    assert first_row_cells[2].text == "2.00"
    assert first_row_cells[3].text == "6.00 €"
    assert first_row_cells[4].text == "24.00 €"
    assert first_row_cells[5].text.strip() == "+100.00%"
    assert _remove_all_whitespace(first_row_cells[6].text) == "+12.00€"

    second_row_cells = table_rows[1]("td")

    assert len(second_row_cells) == 7

    second_holding_link = second_row_cells[0].a

    assert second_holding_link is not None
    assert str(second_holding_link["href"]).endswith(
        f"/p/{portfolio_id}/holdings/{holding_two_id}/edit"
    )
    assert second_row_cells[0].text == "Maple Leaf"
    assert second_row_cells[1].text == "Silver"
    assert second_row_cells[2].text == "3.00"
    assert second_row_cells[3].text == "5.00 €"
    assert second_row_cells[4].text == "30.00 €"
    assert second_row_cells[5].text.strip() == "+100.00%"
    assert _remove_all_whitespace(second_row_cells[6].text) == "+15.00€"

    table_footer = soup.tfoot

    assert table_footer is not None

    footer_cells = table_footer("th")

    assert len(footer_cells) == 4

    assert footer_cells[0].text == "Total"
    assert footer_cells[1].text == "54.00 €"
    assert footer_cells[2].text.strip() == "+100.00%"
    assert _remove_all_whitespace(footer_cells[3].text) == "+27.00€"


def _remove_all_whitespace(text: str) -> str:
    return re.sub(r"\s+", "", text)
