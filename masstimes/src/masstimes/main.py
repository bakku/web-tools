from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import home

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="src/masstimes/static"), name="static")

app.include_router(home.router)
