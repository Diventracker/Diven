from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db


router = APIRouter()
templates = Jinja2Templates(directory="ventas/templates")


#Ruta para la ventana del login
@router.get("/ventas", response_class=HTMLResponse, tags=["ventas"])
def Ventas_get(request: Request):
    return templates.TemplateResponse("ventas.html", {"request": request})