import uuid

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import UUID4

from ..internal.models import Portfolio
from ..internal.repo import add_portfolio, get_portfolio
from .shared import templates

router = APIRouter()


@router.post("/p/")
async def create() -> RedirectResponse:
    portfolio = Portfolio(id=uuid.uuid4(), holdings=[])

    add_portfolio(portfolio)

    return RedirectResponse(f"/p/{portfolio.id}", status_code=303)


@router.get("/p/{_id}")
async def show(_id: UUID4, request: Request) -> HTMLResponse:
    portfolio = get_portfolio(_id)

    return templates.TemplateResponse(
        "portfolios/show.html.jinja2", {"portfolio": portfolio, "request": request}
    )
