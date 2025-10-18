import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .internal.price_cache import get_price_cache
from .routers import holdings, home, portfolios
from .routers.shared import get_template_context, templates

logging.basicConfig(level=os.getenv("LOG_LEVEL", "WARNING").upper())


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    # Application startup
    cache = get_price_cache()
    cache.start_background_refresh()

    yield

    # Application shutdown
    await cache.stop_background_refresh()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> HTMLResponse:
    if exc.status_code == 404:
        context = await get_template_context(request=request)
        return templates.TemplateResponse(
            "404.html.jinja2",
            context,
            status_code=404,
        )

    # For other HTTP exceptions, return the default response
    return HTMLResponse(content=str(exc.detail), status_code=exc.status_code)


app.mount("/static", StaticFiles(directory="src/metals/static"), name="static")

app.include_router(portfolios.router)
app.include_router(holdings.router)
app.include_router(home.router)
