from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from .shared import get_template_context, templates

router = APIRouter()


@router.get("/")
async def home_index(request: Request) -> HTMLResponse:
    context = await get_template_context(request=request)
    return templates.TemplateResponse("home/index.html.jinja2", context)
