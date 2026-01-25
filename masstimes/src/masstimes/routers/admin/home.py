from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from masstimes.routers.shared import templates

router = APIRouter()


@router.get("/")
async def admin_home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="admin/home.html.jinja")
