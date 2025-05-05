#rutas de familiar
#creado por david el 05/05

from app.models import Familiar
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import psycopg2
from psycopg2 import errors
from app.services.dependencies import get_db
from app.models import Familiar
from app.schemas.familiar import (
    FamiliarCreate,
    FamiliarOut,
    UsuarioFamiliarOut
)
from typing import List
from app.utils.helpers import (
    crear_respuesta_json
)


#direccion de todas las rutas de familiares
familiares_router = APIRouter(prefix="/familiares", tags=["Familiares"])


#CREAR FAMILIAR

#ruta post para guardar familiares
#creada por david el 25/04
@familiares_router.post("/registrar-familiar", status_code=status.HTTP_201_CREATED)
def registrar_familiar(familiar: FamiliarCreate, db: Session = Depends(get_db)):
    try:
        nuevo_familiar = Familiar(**familiar.model_dump())
        db.add(nuevo_familiar)
        db.commit()
        db.refresh(nuevo_familiar)

        return crear_respuesta_json(
            status_code=201,
            message="Familiar registrado correctamente"
        )
    except IntegrityError as e:
        db.rollback()

        #captura error de clave unica combinada
        if isinstance(e.orig, psycopg2.errors.UniqueViolation):
            raise HTTPException(
                status_code=400,
                detail="Este familiar ya está registrado para este adulto mayor"
            )

        #captura error de check de que el adulto mayor no puede guardarse como familiar al mismo tiempo
        if isinstance(e.orig, errors.CheckViolation):
            raise HTTPException(
                status_code=400,
                detail="El adulto mayor no puede ser su propio familiar"
            )

        raise HTTPException(
            status_code=500,
            detail="Error de integridad en la base de datos"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al registrar familiar: {str(e)}"
        )

####################################################################################################

#OBTENER FAMILIAR

#ruta get para obtener los familiares de un adulto mayor
#creada por david el 03/05
@familiares_router.get("/familiares-adulto-mayor/{adulto_mayor_id}", response_model=List[FamiliarOut])
def obtener_familiares_adulto_mayor(adulto_mayor_id: int, db: Session = Depends(get_db)):
    try:
        #obtener los familiares del adulto mayor
        familiares = db.query(Familiar).filter(Familiar.adulto_mayor_id == adulto_mayor_id).all()
        familiares_out = []

        for familiar in familiares:
            familiar_rel_schema = UsuarioFamiliarOut(
                id_usuario=familiar.familiar.id,
                nombres=familiar.familiar.nombres,
                apellidos=familiar.familiar.apellidos,
                correo=familiar.familiar.correo,
                telefono=familiar.familiar.telefono,
                foto_perfil=familiar.familiar.foto_perfil
            )
            familiar_out_schema = FamiliarOut(
                id_adulto_mayor=familiar.adulto_mayor_id,
                familiar_rel=familiar_rel_schema
            )
            familiares_out.append(familiar_out_schema)

        return familiares_out
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener los familiares del adulto mayor: {str(e)}"
        )