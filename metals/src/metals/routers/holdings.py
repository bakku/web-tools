import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError
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
from metals.internal.types import Metal
from metals.routers.shared import build_template_context, templates
from metals.routers.types import HoldingForm

router = APIRouter()


def _validate_holding_form(
    description: str, metal: str, quantity: str, purchase_price: str
) -> tuple[HoldingForm | None, dict[str, str]]:
    """
    Validate holding form data.

    Returns:
        Tuple of (validated_form, errors). If validation succeeds, errors dict is
        empty. If validation fails, validated_form is None and errors dict contains
        field errors.
    """
    errors: dict[str, str] = {}
    try:
        metal_enum = Metal(metal)
        form = HoldingForm(
            description=description,
            metal=metal_enum,
            quantity=float(quantity),
            purchase_price=float(purchase_price),
        )
        return form, errors
    except (ValueError, ValidationError) as e:
        if isinstance(e, ValidationError):
            for error in e.errors():
                field = str(error["loc"][-1])
                errors[field] = error["msg"]
        else:
            errors["general"] = str(e)
        return None, errors


@router.get("/p/{portfolio_id}/holdings/new")
async def holdings_new(portfolio_id: uuid.UUID, request: Request) -> HTMLResponse:
    context = await build_template_context(portfolio_id=portfolio_id, request=request)
    return templates.TemplateResponse("holdings/new.html.jinja2", context)


@router.post("/p/{portfolio_id}/holdings", response_model=None)
async def holdings_create(
    portfolio_id: uuid.UUID,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    description: Annotated[str, Form()],
    metal: Annotated[str, Form()],
    quantity: Annotated[str, Form()],
    purchase_price: Annotated[str, Form()],
) -> Response:
    # Validate the form data
    data, errors = _validate_holding_form(description, metal, quantity, purchase_price)

    if errors:
        # Return to form with errors
        context = await build_template_context(
            portfolio_id=portfolio_id,
            request=request,
            errors=errors,
            form_data={
                "description": description,
                "metal": metal,
                "quantity": quantity,
                "purchase_price": purchase_price,
            },
        )
        return templates.TemplateResponse("holdings/new.html.jinja2", context)

    assert data is not None  # For type checker

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
    holding = get_holding(session, portfolio_id, holding_id)

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


@router.post("/p/{portfolio_id}/holdings/{holding_id}", response_model=None)
async def holdings_update(
    portfolio_id: uuid.UUID,
    holding_id: uuid.UUID,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    description: Annotated[str, Form()],
    metal: Annotated[str, Form()],
    quantity: Annotated[str, Form()],
    purchase_price: Annotated[str, Form()],
) -> Response:
    holding = get_holding(session, portfolio_id, holding_id)

    if holding is None:
        raise HTTPException(status_code=404)

    # Validate the form data
    data, errors = _validate_holding_form(description, metal, quantity, purchase_price)

    if errors:
        # Return to form with errors
        context = await build_template_context(
            portfolio_id=portfolio_id,
            holding_id=holding_id,
            holding=holding,
            request=request,
            errors=errors,
            form_data={
                "description": description,
                "metal": metal,
                "quantity": quantity,
                "purchase_price": purchase_price,
            },
        )
        return templates.TemplateResponse("holdings/edit.html.jinja2", context)

    assert data is not None  # For type checker

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
    holding = get_holding(session, portfolio_id, holding_id)

    if holding is None:
        raise HTTPException(status_code=404)

    delete_holding(session, holding)

    return RedirectResponse(f"/p/{portfolio_id}", status_code=303)
