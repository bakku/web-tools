import uuid

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from ..internal.persistency.models import Portfolio
from ..internal.persistency.queries import get_portfolio, insert_portfolio
from ..internal.portfolio_calculations import calculate_portfolio_overview
from ..internal.price_cache import get_price_cache
from .shared import build_template_context, templates

router = APIRouter()


@router.post("/p/")
async def portfolios_create() -> RedirectResponse:
    portfolio = insert_portfolio(Portfolio())

    return RedirectResponse(f"/p/{portfolio.id}", status_code=303)


@router.get("/p/{_id}")
async def portfolios_show(_id: uuid.UUID, request: Request) -> HTMLResponse:
    portfolio = get_portfolio(_id)

    if portfolio is None:
        raise HTTPException(status_code=404)

    try:
        cache = get_price_cache()
        current_prices = await cache.get_prices()
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Unable to fetch current metal prices: {str(e)}",
        )

    portfolio_overview = calculate_portfolio_overview(portfolio, current_prices)

    context = await build_template_context(
        portfolio_id=portfolio.id, data=portfolio_overview, request=request
    )
    return templates.TemplateResponse("portfolios/show.html.jinja2", context)
