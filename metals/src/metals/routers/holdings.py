from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import UUID4, BaseModel

from ..internal.models import Holding, Metal
from ..internal.repo import get_portfolio, update_portfolio
from .shared import templates

router = APIRouter()


@router.get("/p/{portfolio_id}/holdings/new")
async def holdings_new(portfolio_id: UUID4, request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "holdings/new.html.jinja2", {"portfolio_id": portfolio_id, "request": request}
    )


@router.get("/p/{portfolio_id}/holdings/{holding_index}/edit")
async def holdings_edit(
    portfolio_id: UUID4, holding_index: int, request: Request
) -> HTMLResponse:
    portfolio = get_portfolio(portfolio_id)

    if portfolio is None:
        raise HTTPException(status_code=404)

    if holding_index < 0 or holding_index >= len(portfolio.holdings):
        raise HTTPException(status_code=404)

    holding = portfolio.holdings[holding_index]

    return templates.TemplateResponse(
        "holdings/edit.html.jinja2",
        {
            "portfolio_id": portfolio_id,
            "holding_index": holding_index,
            "holding": holding,
            "request": request,
        },
    )


class HoldingsCreateForm(BaseModel):
    description: str
    metal: Metal
    quantity: float
    purchase_price: float


@router.post("/p/{portfolio_id}/holdings")
async def holdings_create(
    portfolio_id: UUID4,
    data: Annotated[HoldingsCreateForm, Form()],
) -> RedirectResponse:
    holding = Holding(
        description=data.description,
        metal=data.metal,
        quantity=data.quantity,
        purchase_price=data.purchase_price,
    )

    portfolio = get_portfolio(portfolio_id)

    if portfolio is None:
        raise HTTPException(status_code=404)

    portfolio.holdings.append(holding)
    update_portfolio(portfolio)

    return RedirectResponse(f"/p/{portfolio_id}", status_code=303)


@router.post("/p/{portfolio_id}/holdings/{holding_index}")
async def holdings_update(
    portfolio_id: UUID4,
    holding_index: int,
    data: Annotated[HoldingsCreateForm, Form()],
) -> RedirectResponse:
    portfolio = get_portfolio(portfolio_id)

    if portfolio is None:
        raise HTTPException(status_code=404)

    if holding_index < 0 or holding_index >= len(portfolio.holdings):
        raise HTTPException(status_code=404)

    portfolio.holdings[holding_index] = Holding(
        description=data.description,
        metal=data.metal,
        quantity=data.quantity,
        purchase_price=data.purchase_price,
    )
    update_portfolio(portfolio)

    return RedirectResponse(f"/p/{portfolio_id}", status_code=303)


@router.post("/p/{portfolio_id}/holdings/{holding_index}/delete")
async def holdings_delete(
    portfolio_id: UUID4,
    holding_index: int,
) -> RedirectResponse:
    portfolio = get_portfolio(portfolio_id)

    if portfolio is None:
        raise HTTPException(status_code=404)

    if holding_index < 0 or holding_index >= len(portfolio.holdings):
        raise HTTPException(status_code=404)

    portfolio.holdings.pop(holding_index)
    update_portfolio(portfolio)

    return RedirectResponse(f"/p/{portfolio_id}", status_code=303)
