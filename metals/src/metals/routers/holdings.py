import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from metals.internal.persistency.db import get_session
from metals.internal.persistency.models import Holding
from metals.internal.persistency.queries import (
    delete_holding,
    get_holding,
    get_portfolio,
    update_holding,
    update_portfolio,
)
from metals.routers.shared import build_template_context, templates
from metals.routers.types import HoldingForm

router = APIRouter()


@router.get("/p/{portfolio_id}/holdings/new")
async def holdings_new(
    portfolio_id: uuid.UUID,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> HTMLResponse:
    """
    Display the form for creating a new holding in a portfolio.

    Args:
        portfolio_id: UUID of the portfolio to add the holding to.
        request: The incoming HTTP request.
        session: Database session for fetching metal prices.

    Returns:
        HTMLResponse rendering the new holding form.
    """
    context = await build_template_context(session, portfolio_id=portfolio_id)
    return templates.TemplateResponse(request, "holdings/new.html.jinja2", context)


@router.post("/p/{portfolio_id}/holdings")
async def holdings_create(
    portfolio_id: uuid.UUID,
    data: Annotated[HoldingForm, Form()],
    session: Annotated[Session, Depends(get_session)],
) -> RedirectResponse:
    """
    Create a new holding in a portfolio.

    Args:
        portfolio_id: UUID of the portfolio to add the holding to.
        data: Form data containing holding details (description, metal,
            quantity, price).
        session: Database session for creating the holding.

    Returns:
        RedirectResponse to the portfolio detail page.

    Raises:
        HTTPException: 404 if portfolio not found.
    """
    holding = Holding(
        description=data.description,
        metal=data.metal,
        quantity=data.quantity,
        purchase_price=data.purchase_price,
    )

    portfolio = get_portfolio(session, portfolio_id)

    if portfolio is None:
        raise HTTPException(status_code=404)

    portfolio.holdings.append(holding)
    update_portfolio(session, portfolio)

    return RedirectResponse(f"/p/{portfolio_id}", status_code=303)


@router.get("/p/{portfolio_id}/holdings/{holding_id}/edit")
async def holdings_edit(
    portfolio_id: uuid.UUID,
    holding_id: uuid.UUID,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> HTMLResponse:
    """
    Display the form for editing an existing holding.

    Args:
        portfolio_id: UUID of the portfolio containing the holding.
        holding_id: UUID of the holding to edit.
        request: The incoming HTTP request.
        session: Database session for fetching the holding.

    Returns:
        HTMLResponse rendering the edit holding form.

    Raises:
        HTTPException: 404 if holding not found.
    """
    holding = get_holding(session, portfolio_id, holding_id)

    if holding is None:
        raise HTTPException(status_code=404)

    context = await build_template_context(
        session,
        portfolio_id=portfolio_id,
        holding_id=holding_id,
        holding=holding,
    )

    return templates.TemplateResponse(
        request,
        "holdings/edit.html.jinja2",
        context,
    )


@router.post("/p/{portfolio_id}/holdings/{holding_id}")
async def holdings_update(
    portfolio_id: uuid.UUID,
    holding_id: uuid.UUID,
    data: Annotated[HoldingForm, Form()],
    session: Annotated[Session, Depends(get_session)],
) -> RedirectResponse:
    """
    Update an existing holding.

    Args:
        portfolio_id: UUID of the portfolio containing the holding.
        holding_id: UUID of the holding to update.
        data: Form data with updated holding details (description, metal,
            quantity, price).
        session: Database session for updating the holding.

    Returns:
        RedirectResponse to the portfolio detail page.

    Raises:
        HTTPException: 404 if holding not found.
    """
    holding = get_holding(session, portfolio_id, holding_id)

    if holding is None:
        raise HTTPException(status_code=404)

    holding.description = data.description
    holding.metal = data.metal
    holding.quantity = data.quantity
    holding.purchase_price = data.purchase_price

    update_holding(session, holding)

    return RedirectResponse(f"/p/{portfolio_id}", status_code=303)


@router.post("/p/{portfolio_id}/holdings/{holding_id}/delete")
async def holdings_delete(
    portfolio_id: uuid.UUID,
    holding_id: uuid.UUID,
    session: Annotated[Session, Depends(get_session)],
) -> RedirectResponse:
    """
    Delete a holding from a portfolio.

    Args:
        portfolio_id: UUID of the portfolio containing the holding.
        holding_id: UUID of the holding to delete.
        session: Database session for deleting the holding.

    Returns:
        RedirectResponse to the portfolio detail page.

    Raises:
        HTTPException: 404 if holding not found.
    """
    holding = get_holding(session, portfolio_id, holding_id)

    if holding is None:
        raise HTTPException(status_code=404)

    delete_holding(session, holding)

    return RedirectResponse(f"/p/{portfolio_id}", status_code=303)
