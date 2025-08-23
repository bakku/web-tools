from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent.parent / "templates"
)


@router.get("/")
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="home.html.jinja")
