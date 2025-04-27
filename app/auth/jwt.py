# Maneja la generación, decodificación y validación de tokens JWT.
# Creado por david el 15/04

from jose import jwt, JWTError
from datetime import datetime, timezone
from app.config import settings
from fastapi import HTTPException, status


#creacion de token
#creado por david el 20/04

def crear_token_acceso(subject: str, additional_data: dict = None) -> str:
    #token sin expiracion
    #subject: el correo de usuario
    #aditional_data: datos adicionales para el payload

    try:
        payload = {
        "sub": subject,
        "iat": datetime.now(timezone.utc), #fecha de creacion
        "app": "TatasApp" #id de la app
        }

        #añadir datos adicionales al payload si los hay
        if additional_data:
            payload.update(additional_data)

        #return: token jwt firmado
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar token: {str(e)}"
        )
