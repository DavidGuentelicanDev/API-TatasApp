#esquemas de alerta
#creado por david el 05/05

from pydantic import BaseModel
from datetime import datetime
from app.utils.helpers import (
    validador_no_string_vacio,
    validador_opcion_en_lista
)


#CREAR ALERTA

# esquema para crear una alerta
# creado por Ale el 02/05/2025
class AlertaCreate(BaseModel):
    usuario_id: int
    ubicacion: str
    mensaje: str
    tipo_alerta: int

    _validar_campos_str = validador_no_string_vacio('ubicacion', 'mensaje')
    _val_tipo = validador_opcion_en_lista("tipo_alerta", [1, 2, 3, 4])

#######################################################################################

#OBTENER ALERTAS

#esquema para obtener alertas por adulto mayor
#creado por Ale 04-05-2025
class AlertaOut(BaseModel):
    id: int
    usuario_id: int
    ubicacion: str
    mensaje: str
    tipo_alerta: int
    fecha_hora: datetime
    estado_alerta: int

    class Config:
        from_attributes = True

######################################################################################

#ACTUALIZAR ALERTA

#esquema para modificar el estado_alerta a 1 (entregada) y respuesta personalizada
#creado por david 04-05-2025
class EstadoAlertaUpdate(BaseModel):
    id: int
    estado_alerta: int = 1

class EstadoAlertaResponse(BaseModel):
    status: str
    message: str