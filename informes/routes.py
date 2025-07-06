from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database.database import get_db
from informes.controller import InformeControlador
from utils.report_generator import generar_pdf_informe


router = APIRouter()

#Ruta para generar informes de los clientes
@router.post("/api/informe-por-cliente", tags=["Informes"])
async def informe_por_cliente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    identificador = data.get("identificador")

    controlador = InformeControlador(db)
    return controlador.generar_informe_por_cliente(identificador)

#generar los informes que estan en el dashboard
@router.post("/api/generar-informe")
async def generar_informe(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    tipo = data["tipo"]
    fecha_inicio_str = data["fecha_inicio"]
    fecha_fin_str = data["fecha_fin"]

    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido")

    controlador = InformeControlador(db)
    try:
        columnas, datos = controlador.generar_informe(tipo, fecha_inicio, fecha_fin)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    path = generar_pdf_informe(tipo, fecha_inicio_str, fecha_fin_str, datos, columnas)
    return FileResponse(path, filename=f"informe_{tipo}.pdf", media_type="application/pdf")
