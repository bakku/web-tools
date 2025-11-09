import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from metals.internal.persistency.db import get_session
from metals.internal.persistency.models import Portfolio
from metals.internal.persistency.queries import (
    get_latest_metal_prices,
    get_portfolio,
    insert_portfolio,
)
from metals.internal.portfolio_calculations import calculate_portfolio_overview
from metals.routers.shared import build_template_context, templates

router = APIRouter()


@router.post("/p/")
async def portfolios_create(
    session: Annotated[Session, Depends(get_session)],
) -> RedirectResponse:
    portfolio = insert_portfolio(session, Portfolio())

    return RedirectResponse(f"/p/{portfolio.id}", status_code=303)


@router.get("/p/{_id}")
async def portfolios_show(
    _id: uuid.UUID,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> HTMLResponse:
    portfolio = get_portfolio(session, _id)

    if portfolio is None:
        raise HTTPException(status_code=404)

    current_prices = get_latest_metal_prices(session)

    if not current_prices:
        raise HTTPException(
            status_code=503,
            detail="Unable to fetch current metal prices from database",
        )

    portfolio_overview = calculate_portfolio_overview(portfolio, current_prices)

    context = await build_template_context(
        session, portfolio_id=portfolio.id, data=portfolio_overview, request=request
    )
    return templates.TemplateResponse("portfolios/show.html.jinja2", context)
