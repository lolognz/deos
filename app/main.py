from fastapi import FastAPI

from app.api.audio import router as audio_router
from app.core.logger import setup_logging

setup_logging()
app = FastAPI(title="DEOS Service")

app.include_router(audio_router, prefix="/audio", tags=["audio"])
