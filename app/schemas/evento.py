#esquemas de evento
#creado por david el 05/05

from pydantic import BaseModel
from datetime import datetime, timezone
from app.utils.helpers import validador_no_string_vacio, validador_fecha_futura, validador_opcion_en_lista


#CREAR EVENTO

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

####################################################################################################

#esquema de respuesta para mostrar evento
#creado por Andrea el 09/05/2025
class EventoOut(BaseModel):
    id: int
    usuario_id: int
    nombre: str
    descripcion: str | None = None
    fecha_hora: datetime
    tipo_evento: int
    tipo_evento_nombre: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        }

####################################################################################################

#esquema para actualizar el evento
#creado por Andrea el 09/05/2025
class EventoUpdate(BaseModel):
    nombre: str
    descripcion: str | None = None
    fecha_hora: datetime
    tipo_evento: int

    _validar_campos_str = validador_no_string_vacio('nombre')
    _val_fecha = validador_fecha_futura("fecha_hora")
    _val_tipo = validador_opcion_en_lista("tipo_evento", [1, 2, 3, 4])