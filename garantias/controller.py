from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory=["templates", "garantias/templates"])

class GarantiaControlador:
    def vista_principal(self, request: Request):
        rol = request.cookies.get("rol")
        return templates.TemplateResponse("garantias.html", {"request": request, "rol": rol})