#rutas de evento
#creado por david el 05/05

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.dependencies import get_db
from app.models import Evento
from app.schemas.evento import (
    EventoCreate,
    EventoOut
)
from typing import List


#direccion de todas las rutas de eventos
eventos_router = APIRouter(prefix="/eventos", tags=["Eventos"])


#CREAR EVENTO

# ruta post para crear eventos
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


# ruta get para listar eventos
# creada por Andrea 9/05/2025
@eventos_router.get("/listar", response_model=List[EventoOut])
def listar_eventos(db: Session = Depends(get_db)):
    eventos = db.query(Evento).all()
    return [
        EventoOut(
            id=e.id,
            usuario_id=e.usuario_id,
            nombre=e.nombre,
            descripcion=e.descripcion,
            fecha_hora=e.fecha_hora,
            tipo_evento=e.tipo_evento,
            tipo_evento_nombre=e.tipo_evento_nombre
        )
        for e in eventos
    ]
# ruta delete para eliminar eventos
# creada por Andrea 9/05/2025
@eventos_router.delete("/eliminar/{evento_id}", status_code=200)
def eliminar_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()

    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    db.delete(evento)
    db.commit()

    return {"status": "success", "message": "Evento eliminado correctamente"}