# Define los esquemas de entrada y salida utilizando Pydantic para validaciones.
# Creado por david el 15/04

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.utils.helpers import (
    validador_no_string_vacio,
    validador_contrasena,
    validador_formato_correo,
    validador_formato_telefono,
    validador_fecha_futura, ############# agregado por andrea 29/04/2025
    validador_opcion_en_lista  ############# agregado por andrea 29/04/2025
)


#clases para mostrar el usuario con direccion (prueba)
#creadas por david el 16/04

class DireccionOut(BaseModel):
    direccion_texto: str
    adicional: Optional[str]

    class Config:
        from_attributes = True

class UsuarioOut(BaseModel):
    nombres: str
    apellidos: str
    fecha_nacimiento: date
    correo: str
    telefono: str
    tipo_usuario_str: str #cambiado para mostrar el nombre del tipo_usuario
    foto_perfil: Optional[str]
    direccion_rel: DireccionOut

    class Config:
        from_attributes = True

####################################################################################################

#esquemas para registrar usuario

#esquema para guardar direccion
#creado por david el 17/04
class DireccionCreate(BaseModel):
    direccion_texto: str
    adicional: Optional[str]

    #validador string vacio
    _validar_campos_str = validador_no_string_vacio(
        'direccion_texto'
    )

#esquema para guardar usuario completo
#creado por david el 17/04
class UsuarioCreate(BaseModel):
    nombres: str
    apellidos: str
    fecha_nacimiento: date
    correo: str
    telefono: str
    tipo_usuario: int
    contrasena: str
    direccion: DireccionCreate

    #validador string no vacio
    _validar_campos_str = validador_no_string_vacio('nombres', 'apellidos', 'correo', 'contrasena')

    #validador de formato contraseña
    _validar_contrasena = validador_contrasena(
        campo='contrasena',
        min_longitud=8,
        requerir_mayuscula=True,
        requerir_numero=True
    )

    #validador de formato correo
    _validar_formato_correo = validador_formato_correo('correo')

    #validador de formato telefono
    _validar_formato_telefono = validador_formato_telefono('telefono')

###########################################################################################################

#esquemas para login

#esquema de datos para el login
#creado por david el 20/04
class UsuarioLogin(BaseModel):
    correo: str
    contrasena: str

#esquema para la respuesta del token
#creado por david el 20/04
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer" #valor por defecto

#esquema para llenar el contenido de la respuesta de login exitoso
#creado por david el 20/04
class ContenidoLogin(BaseModel):
    id_usuario: int
    nombres: str
    tipo_usuario: int
    token: str

#esquema para la respuesta exitosa
#creado por david el 20/04
class RespuestaLoginExitoso(BaseModel):
    status: str = "success"
    message: str = "Credenciales válidas"
    contenido: ContenidoLogin

#esquema para la respuesta erronea
#creado por david el 20/04
class RespuestaLoginErronea(BaseModel):
    status: str = "error"
    message: str = "Credenciales inválidas"

###########################################################################################

#esquema para hacer match con los contactos registrados en el telefono
#creado por david y andrea el 25/04
class ContactosRegistrados(BaseModel):
    id_usuario: int
    telefono: str
    tipo_usuario: int

###########################################################################################

#esquema para guardar familiares
#creado por david el 25/04
class FamiliarCreate(BaseModel):
    adulto_mayor_id: int
    familiar_id: int

##############################################################################################

#esquema para crear evento
#creado por Andrea el 29/04/2025

class EventoCreate(BaseModel):
    usuario_id: int
    nombre: str
    descripcion: str | None = None
    fecha_hora: datetime
    tipo_evento: int

    _validar_campos_str = validador_no_string_vacio('nombre')
    _val_fecha = validador_fecha_futura("fecha_hora")
    _val_tipo = validador_opcion_en_lista("tipo_evento", [1, 2, 3, 4])
