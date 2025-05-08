#rutas de alerta
#creado por david el 05/05

from app.models import Familiar, Usuario
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.services.dependencies import get_db
from app.models import Usuario, Familiar, Alerta
from app.schemas.alerta import (
    AlertaCreate,
    AlertaOut,
    EstadoAlertaUpdate,
    EstadoAlertaResponse
)
from typing import List
from app.utils.helpers import (
    crear_respuesta_json,
    #validar_alerta_ya_entregada
)
from app.services.alertas_services import crear_alerta


#direccion de todas las rutas de alerta
alertas_router = APIRouter(prefix="/alertas", tags=["Alertas"])


#CREAR ALERTA

# ruta POST para crear ALARMAS
#Envía notificacion a familiar si tiene token (PENDIENTE)
# creada por Ale 02/05/2025
@alertas_router.post("/crear-alerta", status_code=status.HTTP_201_CREATED)
def registrar_alerta(alerta: AlertaCreate, db: Session = Depends(get_db)):
    try:
        # 1. Guardar alerta en la base de datos
        nueva_alerta = crear_alerta(alerta, db)

        # 2. Buscar familiares asociados al usuario que generó la alerta
        familiares = db.query(Familiar).filter(Familiar.adulto_mayor_id == alerta.usuario_id).all()

        for f in familiares:
            familiar_usuario = db.query(Usuario).filter(Usuario.id == f.familiar_id).first()

            if familiar_usuario:
                # Cuerpo del mensaje (mensaje + link a ubicación si existe)
                cuerpo = nueva_alerta.mensaje
                if nueva_alerta.ubicacion:
                    cuerpo += f"\nUbicación: https://maps.google.com/?q={nueva_alerta.ubicacion}"

        # 3. Respuesta exitosa
        return crear_respuesta_json(
            status_code=201,
            message="Alerta registrada correctamente",
            data={"id_alerta": nueva_alerta.id}
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al registrar alerta: {str(e)}"
        )

#############################################################################################################

#OBTENER ALERTA

# GET para obtener las alertas asociadas al adulto mayor de un familiar en estado=0
# Creado por Ale el 04/05/2025
@alertas_router.get("/obtener-alertas-pendientes/{id_familiar}", response_model=List[AlertaOut])
def obtener_alertas_por_familiar(id_familiar: int, db: Session = Depends(get_db)):
    try:
        relacion = db.query(Familiar).filter(Familiar.familiar_id == id_familiar).first()
        if not relacion:
            raise HTTPException(status_code=404, detail="No se encontró relación con adulto mayor")

        adulto_mayor_id = relacion.adulto_mayor_id

        alertas = db.query(Alerta).filter(
            Alerta.usuario_id == adulto_mayor_id,
            Alerta.estado_alerta == 0  # Estado 0 indica alerta pendiente
        ).order_by(Alerta.id.asc()).all()

        return alertas  # FastAPI lo formatea automáticamente usando AlertaOut

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener alertas del familiar: {str(e)}"
        )

#ruta GET para obtener todas las alertas de un adulto mayor relacionado en estado = 1 para el historial
#creado por david el 08/05
@alertas_router.get("/obtener-alertas-historial/{id_familiar}", response_model=List[AlertaOut])
def obtener_alertas_por_familiar(id_familiar: int, db: Session = Depends(get_db)):
    try:
        relacion = db.query(Familiar).filter(Familiar.familiar_id == id_familiar).first()
        if not relacion:
            raise HTTPException(status_code=404, detail="No se encontró relación con adulto mayor")

        adulto_mayor_id = relacion.adulto_mayor_id

        alertas = db.query(Alerta).filter(
            Alerta.usuario_id == adulto_mayor_id,
            Alerta.estado_alerta == 1  #estado indica alerta ya notificadada (entregada)
        ).order_by(Alerta.id.asc()).all()

        return alertas

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener alertas del familiar: {str(e)}"
        )

#############################################################################################################

#ACTUALIZAR ALERTA

#ruta PATCH para actualizar el estado de la alerta
#creado por david el 04/05
@alertas_router.patch("/actualizar-estado", response_model=EstadoAlertaResponse, status_code=status.HTTP_200_OK)
def actualizar_estado_alerta(data: EstadoAlertaUpdate, db: Session = Depends(get_db)):
    try:
        alerta = db.query(Alerta).filter(Alerta.id == data.id).first()
        if not alerta:
            return EstadoAlertaResponse(
                status="error",
                message="Alerta no encontrada"
            )

        alerta.estado_alerta = data.estado_alerta
        db.commit()
        db.refresh(alerta)

        return EstadoAlertaResponse(
            status="success",
            message=f"Estado de alerta actualizado correctamente a Entregada ({data.estado_alerta})"
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=EstadoAlertaResponse(
                status="error",
                message=f"Error al actualizar estado de alerta: {str(e)}"
            ).model_dump()
        )