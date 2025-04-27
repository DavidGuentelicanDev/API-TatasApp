# Este archivo servirá para definir funciones de dependencia reutilizables
# Creado por david el 15/04

from app.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Generator

# retorna una sesion de la db, para inyectar en las rutas
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
