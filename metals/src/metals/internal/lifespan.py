from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from .price_cache import get_price_cache


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    # Application startup
    cache = get_price_cache()
    cache.start_background_refresh()

    yield

    # Application shutdown
    await cache.stop_background_refresh()
