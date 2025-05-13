#rutas de usuario
#creado por david el 05/05

from app.models import Usuario
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.settings.dependencies import get_db
from app.models import Usuario, Direccion
from app.schemas.usuario import (
    UsuarioOut,
    UsuarioCreate,
    UsuarioLogin,
    RespuestaLoginExitoso,
    RespuestaLoginErronea,
    ContactosRegistrados,
    FotoPerfilUpdate,
    FotoPerfilOut,
    UsuarioUpdate,
    CorreoUpdate,
    ContrasenaUpdate
)
from app.auth.hashing import get_hash_contrasena
from app.auth.auth import autentificar_usuario
from app.auth.jwt import crear_token_acceso
from typing import List
from app.utils.helpers import verificar_campos_unicos, crear_respuesta_json


#direccion por defecto de todas las rutas de usuarios
usuarios_router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


#CREAR USUARIO

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

#OBTENER USUARIOS

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

#ruta para mostrar usuario completo por id
#creada por david el 04/05
@usuarios_router.get("/{usuario_id}", response_model=UsuarioOut)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return UsuarioOut(
        nombres=usuario.nombres,
        apellidos=usuario.apellidos,
        fecha_nacimiento=usuario.fecha_nacimiento,
        correo=usuario.correo,
        telefono=usuario.telefono,
        tipo_usuario=usuario.tipo_usuario,
        direccion_rel=usuario.direccion_rel
    )

#ruta para obtener la foto de perfil por id (GET)
#creado por david el 09/05
@usuarios_router.get("/foto-perfil/{usuario_id}", response_model=FotoPerfilOut)
def obtener_foto_perfil(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return FotoPerfilOut(
        id_usuario=usuario.id,
        foto_perfil=usuario.foto_perfil
    )

#########################################################################################################

#LOGIN DE USUARIO

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

##################################################################################################

#ACTUALIZAR USUARIO

#ruta PATCH para actualizar la foto de perfil
#creado por david el 09/05
@usuarios_router.patch("/editar-foto-perfil", status_code=status.HTTP_200_OK)
def editar_foto_perfil(data: FotoPerfilUpdate, db: Session = Depends(get_db)):
    try:
        usuario = db.query(Usuario).filter(Usuario.id == data.id).first()
        if not usuario:
            return JSONResponse({
                "status": "error",
                "message": "Usuario no encontrado"
            })

        usuario.foto_perfil = data.foto_perfil
        db.commit()
        db.refresh(usuario)

        return JSONResponse({
            "status": "success",
            "message": "Foto de perfil editada correctamente"
        })

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": f"Error al editar la foto de perfil: {str(e)}"
        })

#ruta PATCH para actualizar datos de usuario (nombres, apellidos, fecha nacimiento, telefono, direccion)
#creado por david el 09/05
@usuarios_router.patch("/editar-datos", status_code=status.HTTP_200_OK)
def editar_datos_usuario(data: UsuarioUpdate, db: Session = Depends(get_db)):
    try:
        usuario = db.query(Usuario).filter(Usuario.id == data.id).first()

        if not usuario:
            return JSONResponse({
                "status": "error",
                "message": "Usuario no encontrado"
            })

        #validar que telefono no este repetido
        verificar_campos_unicos(
            db=db,
            modelo=Usuario,
            campos={"telefono": data.telefono},
            exclusion_id=data.id
        )

        #actualizar datos del usuario
        usuario.nombres = data.nombres
        usuario.apellidos = data.apellidos
        usuario.fecha_nacimiento = data.fecha_nacimiento
        usuario.telefono = data.telefono

        #actualizar datos de direccion
        direccion = db.query(Direccion).filter(Direccion.id == usuario.direccion_id).first()

        if not direccion:
            return JSONResponse({
                "status": "error",
                "message": "Dirección no encontrada"
            })

        direccion.direccion_texto = data.direccion.direccion_texto
        direccion.adicional = data.direccion.adicional

        db.commit()
        db.refresh(usuario)

        return JSONResponse({
            "status": "success",
            "message": "Datos de usuario actualizados correctamente"
        })

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception as e:
        db.rollback()
        return JSONResponse({
            "status": "error",
            "message": f"Error al editar el usuario: {str(e)}"
        })

#ruta PATCH para actualizar correo
#creado por david el 10/05
@usuarios_router.patch("/editar-correo", status_code=status.HTTP_200_OK)
def editar_correo(data: CorreoUpdate, db: Session = Depends(get_db)):
    try:
        usuario = db.query(Usuario).filter(Usuario.id == data.id).first()

        if not usuario:
            return JSONResponse({
                "status": "error",
                "message": "Usuario no encontrado"
            })

        #validar que correo no este repetido
        verificar_campos_unicos(
            db=db,
            modelo=Usuario,
            campos={"correo": data.correo},
            exclusion_id=data.id
        )

        usuario.correo = data.correo
        db.commit()
        db.refresh(usuario)

        return JSONResponse({
            "status": "success",
            "message": "Correo editado correctamente"
        })

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": f"Error al editar el correo: {str(e)}"
        })

#ruta PATCH para editar contraseña
#creado por david el 10/05
@usuarios_router.patch("/editar-contrasena", status_code=status.HTTP_200_OK)
def editar_contrasena(data: ContrasenaUpdate, db: Session = Depends(get_db)):
    try:
        usuario = db.query(Usuario).filter(Usuario.id == data.id).first()

        if not usuario:
            return JSONResponse({
                "status": "error",
                "message": "Usuario no encontrado"
            })

        contrasena = get_hash_contrasena(data.contrasena)

        usuario.contrasena = contrasena
        db.commit()
        db.refresh(usuario)

        return JSONResponse({
            "status": "success",
            "message": "Contraseña editada correctamente"
        })

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": f"Error al editar la contraseña: {str(e)}"
        })