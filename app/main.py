# Punto de entrada FastAPI
# Creado por david el 15/04

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from app.database import Base, engine
from app.routers import usuarios_router, familiares_router, eventos_router
from app.validations import (
    handler_validacion_excepciones_personalizadas,
    handler_excepciones_http_peronalizadas
)
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.utils.notifications import inicializar_firebase


app = FastAPI(title=settings.PROJECT_NAME) #inicializar la app

Base.metadata.create_all(bind=engine) #crea las tablas automaticamente al iniciar

firebase_status = inicializar_firebase() #inicializa firebase admin sdk

#cors middleware para la ruta local/externa de la api
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#ruta raiz para verificar que la api funciona
@app.get("/")
def root():
    return {
        "mensaje": "API TatasApp iniciada correctamente",
        "firebase_status": firebase_status
    }

#incluye todas las rutas de manera modular de routers.py automaticamente
app.include_router(usuarios_router)
app.include_router(familiares_router)
app.include_router(eventos_router)

#agregados los handlers
app.add_exception_handler(RequestValidationError, handler_validacion_excepciones_personalizadas)
app.add_exception_handler(HTTPException, handler_excepciones_http_peronalizadas)
