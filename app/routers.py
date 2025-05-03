# Define las rutas principales de la API y agrupa los endpoints por funcionalidades.
# Creado por david el 15/04
from pydantic import BaseModel
from app.models import Familiar, Usuario
from app.utils.notifications import enviar_notificacion_push
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import psycopg2
from psycopg2 import errors
from app.services.dependencies import get_db
from app.models import Usuario, Direccion, Familiar, Evento
from app.schemas import (
    UsuarioOut,
    UsuarioCreate,
    UsuarioLogin,
    RespuestaLoginExitoso,
    RespuestaLoginErronea,
    ContactosRegistrados,
    FamiliarCreate,
    EventoCreate,
    TokenPushIn,
    FamiliarOut,
    UsuarioFamiliarOut
)
from app.auth.hashing import get_hash_contrasena
from app.auth.auth import autentificar_usuario
from app.auth.jwt import crear_token_acceso
from typing import List
from app.utils.helpers import (
    verificar_campos_unicos,
    crear_respuesta_json
)
from app.schemas import AlertaCreate
from app.services.alertas_services import crear_alerta


usuarios_router = APIRouter(prefix="/usuarios", tags=["Usuarios"]) #direccion por defecto de todas las rutas de usuarios
familiares_router = APIRouter(prefix="/familiares", tags=["Familiares"]) #direccion de todas las rutas de familiares
eventos_router = APIRouter(prefix="/eventos", tags=["Eventos"]) #direccion de todas las rutas de eventos
alertas_router = APIRouter(prefix="/alertas", tags=["Alertas"]) #direccion de todas las rutas de alerta


#ruta de prueba para usuarios
#creada por david el 16/04
@usuarios_router.get("/", response_model=List[UsuarioOut])
def obtener_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()

    #se construye la respuesta agregando tipo_usuario_str a cada usuario
    usuarios_out = []
    for usuario in usuarios:
        usuario_dict = UsuarioOut(
            nombres=usuario.nombres,
            apellidos=usuario.apellidos,
            fecha_nacimiento=usuario.fecha_nacimiento,
            correo=usuario.correo,
            telefono=usuario.telefono,
            tipo_usuario_str=usuario.tipo_usuario_nombre,
            foto_perfil=usuario.foto_perfil,
            direccion_rel=usuario.direccion_rel
        )
        usuarios_out.append(usuario_dict)

    return usuarios_out

#########################################################################################################

#ruta para registrar usuario
#creada por david el 17/04
@usuarios_router.post("/registro_usuario", status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    #verifica si ya existe usuario con ese correo o telefono (campos unique)
    verificar_campos_unicos(
        db=db,
        modelo=Usuario,
        campos={
            "correo": usuario.correo,
            "telefono": usuario.telefono
        }
    )

    try:
        #crear direccion
        nueva_direccion = Direccion(**usuario.direccion.model_dump())
        db.add(nueva_direccion)
        db.flush()

        #crear usuario
        usuario_data = usuario.model_dump(exclude={"direccion", "contrasena"})
        nuevo_usuario = Usuario(
            **usuario_data,
            direccion_id=nueva_direccion.id,
            contrasena=get_hash_contrasena(usuario.contrasena)
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        return crear_respuesta_json(
            status_code=201,
            message="Usuario registrado correctamente"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al registrar usuario: {str(e)}"
        )

######################################################################################################

#ruta para login
#creado por david el 20/04
@usuarios_router.post("/login")
async def login(datos_login: UsuarioLogin, db: Session = Depends(get_db)):
    #autenticar usuario
    usuario = autentificar_usuario(db, datos_login.correo, datos_login.contrasena)

    #login erroneo
    if not usuario:
        respuesta = RespuestaLoginErronea()
        return JSONResponse(status_code=200, content=respuesta.model_dump())

    #datos adicionales del token
    token_data = {
        "id_usuario": usuario.id,
        "nombres": usuario.nombres,
        "tipo_usuario": usuario.tipo_usuario
    }

    #generar token
    token = crear_token_acceso(subject=usuario.correo, additional_data=token_data)

    #preparar el contenido
    contenido = {
        "id_usuario": usuario.id,
        "nombres": usuario.nombres,
        "tipo_usuario": usuario.tipo_usuario,
        "token": token
    }

    #respuesta login exitoso
    respuesta = RespuestaLoginExitoso(contenido=contenido)

    return JSONResponse(status_code=200, content=respuesta.model_dump())

#######################################################################################################

#ruta get para obtener los usuarios registrados tipo familiar (1)
#creada por david y andrea el 25/04
@usuarios_router.get("/contactos-registrados", response_model=List[ContactosRegistrados])
def contactos_familiares_registrados(db: Session = Depends(get_db)):
    usuarios_familiares = db.query(Usuario).filter(Usuario.tipo_usuario == 2).all()

    #se construye la respuesta agregando tipo_usuario_str a cada usuario
    contactos_registrados_out = []
    for usuario in usuarios_familiares:
        usuario_dict = ContactosRegistrados(
            id_usuario=usuario.id,
            telefono=usuario.telefono,
            tipo_usuario=usuario.tipo_usuario
        )
        contactos_registrados_out.append(usuario_dict)

    return contactos_registrados_out

####################################################################################################

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

#######################################################################################################

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

######################################################################################################

# ruta POST para crear ALARMAS
#Envía notificacion a familiar si tiene token
# creada por Ale 02/05/2025
@alertas_router.post("/crear", status_code=status.HTTP_201_CREATED)
def registrar_alerta(alerta: AlertaCreate, db: Session = Depends(get_db)):
    try:
        # 1. Guardar alerta en la base de datos
        nueva_alerta = crear_alerta(alerta, db)

        # 2. Buscar familiares asociados al usuario que generó la alerta
        familiares = db.query(Familiar).filter(Familiar.adulto_mayor_id == alerta.usuario_id).all()

        for f in familiares:
            familiar_usuario = db.query(Usuario).filter(Usuario.id == f.familiar_id).first()
            if familiar_usuario and familiar_usuario.token_push:
                titulo = "Alerta de emergencia"
                cuerpo = f"Se ha generado una alerta: {nueva_alerta.tipo_alerta_nombre}"
                enviar_notificacion_push(familiar_usuario.token_push, titulo, cuerpo)

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

# POST PARA REGISTRATR TOKEN
# creada por Ale 02/05/2025
@usuarios_router.post("/registrar_token_push", status_code=200)
def registrar_token_push(data: TokenPushIn, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == data.id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.token_push = data.token_push
    db.commit()

    return {
        "status": "success",
        "message": "Token push registrado correctamente"
    }

###############################################################################################