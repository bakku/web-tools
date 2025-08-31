from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import home, portfolios

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/metals/static"), name="static")

app.include_router(portfolios.router)
app.include_router(home.router)
