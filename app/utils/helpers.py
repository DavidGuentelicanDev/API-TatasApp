# Funciones generales de utilidad: validaciones, generadores de códigos, formateo de datos, etc.
# Validar formato de email
# Convertir datos entre formatos (ej: dict a JSON con reglas especiales)
# Generar códigos únicos

# Creado por david el 15/04

from pydantic import field_validator
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import re
from datetime import datetime, timezone


#SCHEMAS DE REGISTRO DE USUARIO

MIN_CONTRASENA = 8

#valida que un string no este vacio o solo con espacios
#creado por david el 17/04
def no_string_vacio(v: str, field_name: str = 'campo') -> str:
    if not v or not v.strip():
        raise ValueError(f"El campo '{field_name}' no puede estar vacío")
    return v.strip()

#decorador no_string_vacio
def validador_no_string_vacio(*campos: str):
    return field_validator(*campos)(lambda cls, v, info: no_string_vacio(v, info.field_name))

#valida la fortaleza de la contraseña
#creado por david el 17/04
def fortalecer_contrasena(
    contrasena: str, 
    min_longitud: int = MIN_CONTRASENA,
    requerir_mayuscula: bool = True,
    requerir_numero: bool = True
) -> str:
    if len(contrasena) < min_longitud:
        raise ValueError(f"La contraseña debe tener al menos {min_longitud} caracteres")
    if requerir_mayuscula and not any(c.isupper() for c in contrasena):
        raise ValueError("La contraseña debe contener al menos una mayúscula")
    if requerir_numero and not any(c.isdigit() for c in contrasena):
        raise ValueError("La contraseña debe contener al menos un número")
    return contrasena

#decorador fortalecer_contrasena
def validador_contrasena(
    campo: str = 'contrasena',
    min_longitud: int = MIN_CONTRASENA,
    requerir_mayuscula: bool = True,
    requerir_numero: bool = True
):
    return field_validator(campo)(
        lambda cls, v, info: fortalecer_contrasena(
            v,
            min_longitud=min_longitud,
            requerir_mayuscula=requerir_mayuscula,
            requerir_numero=requerir_numero
        )
    )

#valida el formato de correo
#creado por david el 18/04
def formato_correo_valido(correo: str) -> str:
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(patron, correo):
        raise ValueError("El formato de correo electrónico no es válido")
    return correo

#decorador para validar el formato de correo
def validador_formato_correo(campo: str = 'correo'):
    return field_validator(campo)(lambda cls, v, info: formato_correo_valido(v))

#valida el formato de telefono
#creado por david el 18/04
def formato_telefono_valido(telefono: str) -> str:
    if not re.match(r'^9\d{8}$', telefono):
        raise ValueError("El teléfono debe tener formato 9XXXXXXXX (9 dígitos)")
    return telefono

#decorador para validar formato telefono
def validador_formato_telefono(campo: str = 'telefono'):
    return field_validator(campo)(lambda cls, v, info: formato_telefono_valido(v))

###################################################################################################

#RUTAS DE REGISTRO DE USUARIOS

#verifica campos unique
#creado por david el 18/04
def verificar_campos_unicos(
    db: Session,
    modelo: type,
    campos: dict,
    exclusion_id: int = None
) -> None:
    for campo, valor in campos.items():
        query = db.query(modelo).filter(getattr(modelo, campo) == valor)
        if exclusion_id:
            query = query.filter(modelo.id != exclusion_id)
        if query.first():
            raise HTTPException(
                status_code=400,
                detail=f"{campo.capitalize()} ya registrado"
            )

#estandariza las respuestas json
#creado por david el 18/04
def crear_respuesta_json(
    status_code: int = 200,
    status: str = "success",
    message: str = "",
    data: dict = None
) -> JSONResponse :
    content = {"status": status, "message": message}
    if data:
        content.update({"data": data})
    return JSONResponse(status_code=status_code, content=content)

#########################################################################

#validador fecha y tiempo 
#agregado por andrea 29/04/2025

def fecha_futura_valida(fecha: datetime, field_name: str = 'fecha') -> datetime:
    ahora = datetime.now().replace(tzinfo=None)
    if fecha < ahora:
        raise ValueError(f"La {field_name} debe ser igual o posterior a la fecha y hora actual")
    return fecha

# Decorador reutilizable para fechas futuras
def validador_fecha_futura(campo: str = 'fecha'):
    return field_validator(campo)(lambda cls, v, info: fecha_futura_valida(v, info.field_name))

# Validar que el valor esté dentro de una lista permitida
def opcion_en_lista_valida(v: int, opciones: list[int], field_name: str = 'campo') -> int:
    if v not in opciones:
        raise ValueError(f"El {field_name} debe ser una de las siguientes opciones: {opciones}")
    return v

# Decorador para ver si la opcion de tipo evento esta dentro ded la lista permitida, 
def validador_opcion_en_lista(campo: str, opciones: list[int]):
    return field_validator(campo)(lambda cls, v, info: opcion_en_lista_valida(v, opciones, info.field_name))
