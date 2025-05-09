#esquemas de usuario
#creado por david el 05/05

from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.utils.helpers import (
    validador_no_string_vacio,
    validador_contrasena,
    validador_formato_correo,
    validador_formato_telefono
)


#REGISTRO DE USUARIO

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

#OBTENER INFO DE USUARIOS

#clases para mostrar el usuario con direccion
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
    tipo_usuario: int #cambiado para mostrar el nombre del tipo_usuario
    direccion_rel: DireccionOut

    class Config:
        from_attributes = True

#esquema para hacer match con los contactos registrados en el telefono
#creado por david y andrea el 25/04
class ContactosRegistrados(BaseModel):
    id_usuario: int
    telefono: str
    tipo_usuario: int

#esquema para consultar la foto de perfil (separado de la consulta general de usuario)
#creado por david el 09/05
class FotoPerfilOut(BaseModel):
    id_usuario: int
    foto_perfil: Optional[str]

###########################################################################################

#LOGIN DE USUARIO

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

#######################################################################################################

#ACTUALIZAR USUARIO

#esquema para editar la foto de perfil
#creado por david el 09/05
class FotoPerfilUpdate(BaseModel):
    id: int
    foto_perfil: str