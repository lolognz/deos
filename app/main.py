from fastapi import FastAPI

from app.api.audio import router as audio_router
from app.api.classify import router as classify_router
from app.api.process import router as process_router
from app.core.logger import setup_logging

setup_logging()
app = FastAPI(title="DEOS Service")

app.include_router(audio_router, prefix="/audio", tags=["audio"])
app.include_router(process_router, prefix="", tags=["process"])
app.include_router(classify_router, prefix="", tags=["classification"])
