from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

templates = Jinja2Templates(directory="templates")  # Ruta donde están las vistas

@router.get("/", response_class=HTMLResponse, tags=["Homepage"])
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})