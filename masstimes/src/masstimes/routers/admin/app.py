from fastapi import Depends, FastAPI

from masstimes.routers.admin import home, jobs
from masstimes.routers.admin.auth import authorize

admin_app = FastAPI(docs_url=None, redoc_url=None, dependencies=[Depends(authorize)])

admin_app.include_router(home.router)
admin_app.include_router(jobs.router)
