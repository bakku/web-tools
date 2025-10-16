from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from .shared import templates

router = APIRouter()


@router.get("/")
async def home_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("home/index.html.jinja2", {"request": request})
