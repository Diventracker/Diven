from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db


router = APIRouter()
templates = Jinja2Templates(directory="dashboard/templates")


#Ruta para la ventana del login
@router.get("/dashboard", response_class=HTMLResponse, tags=["dashboard"])
def dashboard_get(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})