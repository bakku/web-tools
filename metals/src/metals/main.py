from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from metals.internal.price_cache import get_price_refresher
from metals.routers import holdings, home, portfolios
from metals.routers.shared import templates


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """
    Manage the application lifecycle.

    Starts the price refresh background task on startup and stops it on shutdown.

    Args:
        _app: The FastAPI application instance (unused).

    Yields:
        None during application runtime.
    """
    # Application startup
    refresher = get_price_refresher()
    refresher.start_background_refresh()

    yield

    # Application shutdown
    await refresher.stop_background_refresh()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> HTMLResponse:
    """
    Handle HTTP exceptions with custom error pages.

    Args:
        request: The incoming HTTP request.
        exc: The HTTP exception that was raised.

    Returns:
        HTMLResponse with custom 404 page for 404 errors, or default error
        response for other HTTP exceptions.
    """
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
