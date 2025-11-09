from typing import Annotated

from fastapi import APIRouter, Request
from fastapi.params import Depends
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
    context = await build_template_context(session, request=request)
    return templates.TemplateResponse("home/index.html.jinja2", context)
