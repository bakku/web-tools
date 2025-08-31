from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="src/metals/static"), name="static")
templates = Jinja2Templates(directory="src/metals/templates")


@app.get("/")
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})
