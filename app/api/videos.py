from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.db import crud
from app.db.session import SessionLocal

router = APIRouter(tags=["videos"])


# ——— Esquemas Pydantic ———

class ClassificationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    tag: str
    score: float
    created_at: datetime


class SummarySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    level: str
    text: str
    created_at: datetime


class TranscriptSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    text: str
    created_at: datetime


class AudioSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    path: str
    created_at: datetime


class VideoListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    url: str
    title: str
    duration: int
    topic: str
    created_at: datetime


class VideoDetail(VideoListItem):
    audio: AudioSchema
    transcript: TranscriptSchema
    summary: SummarySchema
    classifications: List[ClassificationSchema]


# ——— Dependencia para obtener la sesión DB ———

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ——— Endpoints ———

@router.get("/", response_model=List[VideoListItem])
def list_videos(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1),
        topic: Optional[str] = Query(None, description="Filtra por campo topic"),
        tag: Optional[str] = Query(None, description="Filtra por clasificación (tag)"),
        date_from: Optional[datetime] = Query(
            None,
            description="Fecha mínima (inclusive) en formato ISO, p.ej. 2025-06-01T00:00:00"
        ),
        date_to: Optional[datetime] = Query(
            None,
            description="Fecha máxima (inclusive) en formato ISO, p.ej. 2025-06-30T23:59:59"
        ),
        db: Session = Depends(get_db)
):
    """
    Lista los vídeos procesados, con paginación y filtros opcionales:
      - topic: exact match en Video.topic
      - tag:   classification.tag
      - date_from / date_to: rango de Video.created_at
    """
    videos = crud.get_videos(
        db,
        skip=skip,
        limit=limit,
        topic=topic,
        tag=tag,
        date_from=date_from,
        date_to=date_to,
    )
    return videos


@router.get("/{video_id}", response_model=VideoDetail)
def get_video(video_id: int, db: Session = Depends(get_db)):
    """
    Devuelve todos los datos de un vídeo por su ID.
    """
    video = crud.get_video_by_id(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video
