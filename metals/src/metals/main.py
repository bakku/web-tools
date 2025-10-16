from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .routers import holdings, home, portfolios
from .routers.shared import templates

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> HTMLResponse:
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "404.html.jinja2",
            {"request": request},
            status_code=404,
        )

    # For other HTTP exceptions, return the default response
    return HTMLResponse(content=str(exc.detail), status_code=exc.status_code)


app.mount("/static", StaticFiles(directory="src/metals/static"), name="static")

app.include_router(portfolios.router)
app.include_router(holdings.router)
app.include_router(home.router)
