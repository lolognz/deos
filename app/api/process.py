from typing import List
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from app.api.classify import TagScore
from app.services.orchestrator import process_audio_url

router = APIRouter()


class ProcessRequest(BaseModel):
    url: HttpUrl
    topic: Optional[str] = None
    summary_level: Optional[str] = "medium"


class ProcessResponse(BaseModel):
    url: str
    audio_path: str
    transcript: str
    summary: str
    topic: Optional[str]
    tags: List[TagScore]


@router.post("/process", response_model=ProcessResponse, status_code=200)
async def process_endpoint(req: ProcessRequest):
    """
    Endpoint único que ejecuta el pipeline completo:
      • Descarga audio
      • Transcribe
      • Resume
      • Devuelve todo junto, con el topic si se proporcionó
    """
    try:
        result = process_audio_url(
            youtube_url=str(req.url),
            topic=req.topic,
            summary_level=req.summary_level
        )
        return result
    except Exception as e:
        # Captura errores inesperados y devuelve 500
        raise HTTPException(status_code=500, detail=str(e))
