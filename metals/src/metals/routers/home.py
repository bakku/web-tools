from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from metals.internal.persistency.db import get_session
from metals.routers.shared import build_template_context, templates

router = APIRouter()


@router.get("/")
async def home_index(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> HTMLResponse:
    """
    Render the home page.

    Args:
        request: The incoming HTTP request.
        session: Database session for fetching metal prices.

    Returns:
        HTMLResponse rendering the home page template.
    """
    context = await build_template_context(session)
    return templates.TemplateResponse(request, "home/index.html.jinja2", context)
