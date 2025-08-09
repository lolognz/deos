from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.audio import router as audio_router
from app.api.classify import router as classify_router
from app.api.ingestion import router as ingestion_router
from app.api.process import router as process_router
from app.api.videos import router as videos_router
from app.core.logger import setup_logging
from app.db import init_db

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Se ejecuta al arrancar FastAPI
    yield


app = FastAPI(
    title="DEOS Service",
    lifespan=lifespan
)

# Configuración de CORS
origins = [
    "http://localhost:5173",  # Tu frontend en desarrollo
    "http://127.0.0.1:5173",  # Alternativa local
    # Aquí puedes añadir el dominio de producción más adelante
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos: GET, POST, PUT, DELETE...
    allow_headers=["*"],  # Permitir todas las cabeceras
)

# Rutas
app.include_router(audio_router, prefix="/audio", tags=["audio"])
app.include_router(process_router, prefix="", tags=["process"])
app.include_router(classify_router, prefix="", tags=["classification"])
app.include_router(videos_router, prefix="/videos", tags=["videos"])
app.include_router(ingestion_router, prefix="/ingest", tags=["ingestion"])
