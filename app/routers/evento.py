#rutas de evento
#creado por david el 05/05

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.dependencies import get_db
from app.models import Evento
from app.schemas.evento import (
    EventoCreate
)


#direccion de todas las rutas de eventos
eventos_router = APIRouter(prefix="/eventos", tags=["Eventos"])


#CREAR EVENTO

# ruta get para crear eventos
# creada por Andrea 29/04/2025
@eventos_router.post("/crear-evento", status_code=status.HTTP_201_CREATED)
def crear_evento(evento: EventoCreate, db: Session = Depends(get_db)):
    try:
        nuevo_evento = Evento(**evento.model_dump())
        db.add(nuevo_evento)
        db.commit()
        db.refresh(nuevo_evento)

        return {
            "status": "success",
            "message": "Evento creado correctamente",
            "evento_id": nuevo_evento.id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear evento: {str(e)}"
        )