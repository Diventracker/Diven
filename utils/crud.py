from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Type, Any

#Funcion crud, crear un nuevo recurso 
def crear_recurso(
    model_class: Type[Any],
    data: dict,
    db: Session,
    redirect_url: str,
    error_url: str,
    on_success=None  
):
    try:
        recurso = model_class(**data)
        db.add(recurso)
        db.commit()
        db.refresh(recurso)

        if on_success:
            on_success(recurso)  # Aquí puedes enviar el correo

        return RedirectResponse(url=redirect_url, status_code=303)
    
    except IntegrityError:
        db.rollback()
        return RedirectResponse(url=f"{error_url}?error=2", status_code=303)
    
    except ValueError as e:
        db.rollback()
        if str(e) == "nombre":
            return RedirectResponse(url=f"{error_url}?error=1", status_code=303)
        return RedirectResponse(url=f"{error_url}?error=generic", status_code=303)


