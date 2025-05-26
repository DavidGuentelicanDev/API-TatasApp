#rutas de evento
#creado por david el 05/05

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.settings.dependencies import get_db
from app.models import Evento, Familiar
from app.schemas.evento import EventoCreate, EventoOut
from typing import List
from app.schemas.evento import EventoUpdate
from fastapi import Query


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

#######################################################################################################

# ruta get para listar eventos
# creada por Andrea 9/05/2025
@eventos_router.get("/listar", response_model=List[EventoOut])
def listar_eventos(
    usuario_id: int = Query(..., description="ID del usuario logueado"),
    db: Session = Depends(get_db)
):
    eventos = db.query(Evento).filter(Evento.usuario_id == usuario_id).all()

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

#######################################################################################################

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

# ruta para modificar eventos
# creada por Andrea 9/05/2025
@eventos_router.put("/modificar/{evento_id}", status_code=200)
def modificar_evento(evento_id: int, datos: EventoUpdate, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()

    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    for campo, valor in datos.model_dump().items():
        setattr(evento, campo, valor)

    db.commit()
    db.refresh(evento)

    return {
        "status": "success",
        "message": "Evento modificado correctamente",
        "evento_id": evento.id
    }

#######################################################################################################

# ruta para traer eventos del adulto mayor segun id familiar
# creada por Andrea 9/05/2025
@eventos_router.get("/listar-por-familiar", response_model=List[EventoOut])
def listar_eventos_por_familiar(
    familiar_id: int = Query(..., description="ID del usuario familiar"),
    db: Session = Depends(get_db)
):
    relacion = db.query(Familiar).filter(Familiar.familiar_id == familiar_id).first()

    if not relacion:
        raise HTTPException(status_code=404, detail="No se encontró adulto mayor asociado")

    eventos = db.query(Evento).filter(Evento.usuario_id == relacion.adulto_mayor_id).all()

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

@eventos_router.get("/proximos", response_model=List[EventoOut])
def obtener_eventos_proximos(
    usuario_id: int = Query(..., description="ID del usuario logueado"),
    minutos: int = Query(15, description="Minutos hacia el futuro para buscar eventos"),
    db: Session = Depends(get_db)
):
    from datetime import datetime, timedelta

    ahora = datetime.now()
    en_minutos = ahora + timedelta(minutes=minutos)

    eventos = db.query(Evento).filter(
        Evento.usuario_id == usuario_id,
        Evento.fecha_hora >= ahora,
        Evento.fecha_hora <= en_minutos
    ).all()

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