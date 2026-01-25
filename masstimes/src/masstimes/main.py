from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from masstimes.bootstrap import bootstrap
from masstimes.routers import home
from masstimes.routers.admin.app import admin_app

bootstrap()


app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="src/masstimes/static"), name="static")
app.mount("/admin", admin_app)

app.include_router(home.router)
