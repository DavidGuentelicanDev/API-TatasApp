#esquemas de familiar
#creado por david el 05/05

from pydantic import BaseModel
from typing import Optional


#REGISTRAR FAMILIARES

#esquema para guardar familiares
#creado por david el 25/04
class FamiliarCreate(BaseModel):
    adulto_mayor_id: int
    familiar_id: int

#########################################################################################

#OBTENER INFO DE FAMILIARES

#esquemas para obtener los familiares registrados en el grupo familiar del adulto mayor
#creado por david el 03/05
class UsuarioFamiliarOut(BaseModel):
    id_usuario: int
    nombres: str
    apellidos: str
    correo: str
    telefono: str
    foto_perfil: Optional[str]

    class Config:
        from_attributes = True

class FamiliarOut(BaseModel):
    id_adulto_mayor: int
    familiar_rel: UsuarioFamiliarOut

    class Config:
        from_attributes = True