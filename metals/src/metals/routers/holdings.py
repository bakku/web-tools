import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from ..internal.persistency.models import Holding
from ..internal.persistency.queries import (
    delete_holding,
    get_holding,
    get_portfolio,
    update_holding,
    update_portfolio,
)
from .shared import build_template_context, templates
from .types import HoldingForm

router = APIRouter()


@router.get("/p/{portfolio_id}/holdings/new")
async def holdings_new(portfolio_id: uuid.UUID, request: Request) -> HTMLResponse:
    context = await build_template_context(portfolio_id=portfolio_id, request=request)
    return templates.TemplateResponse("holdings/new.html.jinja2", context)


@router.post("/p/{portfolio_id}/holdings")
async def holdings_create(
    portfolio_id: uuid.UUID,
    data: Annotated[HoldingForm, Form()],
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


@router.get("/p/{portfolio_id}/holdings/{holding_id}/edit")
async def holdings_edit(
    portfolio_id: uuid.UUID, holding_id: uuid.UUID, request: Request
) -> HTMLResponse:
    holding = get_holding(portfolio_id, holding_id)

    if holding is None:
        raise HTTPException(status_code=404)

    context = await build_template_context(
        portfolio_id=portfolio_id,
        holding_id=holding_id,
        holding=holding,
        request=request,
    )

    return templates.TemplateResponse(
        "holdings/edit.html.jinja2",
        context,
    )


@router.post("/p/{portfolio_id}/holdings/{holding_id}")
async def holdings_update(
    portfolio_id: uuid.UUID,
    holding_id: uuid.UUID,
    data: Annotated[HoldingForm, Form()],
) -> RedirectResponse:
    holding = get_holding(portfolio_id, holding_id)

    if holding is None:
        raise HTTPException(status_code=404)

    holding.description = data.description
    holding.metal = data.metal
    holding.quantity = data.quantity
    holding.purchase_price = data.purchase_price
    holding.updated_at = datetime.now()

    update_holding(holding)

    return RedirectResponse(f"/p/{portfolio_id}", status_code=303)


@router.post("/p/{portfolio_id}/holdings/{holding_id}/delete")
async def holdings_delete(
    portfolio_id: uuid.UUID,
    holding_id: uuid.UUID,
) -> RedirectResponse:
    holding = get_holding(portfolio_id, holding_id)

    if holding is None:
        raise HTTPException(status_code=404)

    delete_holding(holding)

    return RedirectResponse(f"/p/{portfolio_id}", status_code=303)
