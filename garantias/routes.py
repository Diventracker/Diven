from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="garantias/templates")


#Ruta para la ventana del login
@router.get("/garantias", response_class=HTMLResponse, tags=["garantias"])
def login_get(request: Request):
    return templates.TemplateResponse("garantias.html", {"request": request})