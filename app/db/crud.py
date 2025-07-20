from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.db import models


def get_video_by_url(db: Session, url: str) -> Optional[models.Video]:
    return db.query(models.Video).filter(models.Video.url == url).first()


def get_video_by_id(db: Session, video_id: int) -> Optional[models.Video]:
    return db.query(models.Video).filter(models.Video.id == video_id).first()


def get_videos(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        topic: Optional[str] = None,
        tag: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
) -> List[models.Video]:
    """
    Lista vídeos con filtros opcionales.
    """
    query = db.query(models.Video)

    if topic:
        query = query.filter(models.Video.topic == topic)
    if date_from:
        query = query.filter(models.Video.created_at >= date_from)
    if date_to:
        query = query.filter(models.Video.created_at <= date_to)
    if tag:
        query = query.join(models.Classification).filter(models.Classification.tag == tag).distinct()

    return query.offset(skip).limit(limit).all()


def create_video(
        db: Session,
        url: str,
        title: str,
        duration: int,
        topic: str
) -> models.Video:
    v = models.Video(url=url, title=title, duration=duration, topic=topic)
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


def create_audio(db: Session, video_id: int, path: str) -> models.Audio:
    a = models.Audio(video_id=video_id, path=path)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


def create_transcript(db: Session, video_id: int, text: str) -> models.Transcript:
    t = models.Transcript(video_id=video_id, text=text)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


def get_document_by_path(db: Session, path: str) -> Optional[models.Document]:
    return db.query(models.Document).filter(models.Document.path == path).first()


def create_document(db: Session, path: str, topic: str) -> models.Document:
    d = models.Document(path=path, topic=topic)
    db.add(d)
    db.commit()
    db.refresh(d)
    return d


def create_summary(
        db: Session,
        *,
        video_id: Optional[int] = None,
        document_id: Optional[int] = None,
        level: str,
        text: str
) -> models.Summary:
    """
    Crea un resumen ligado a un vídeo o a un documento.
    Debe pasarse video_id o document_id.
    """
    s = models.Summary(
        video_id=video_id,
        document_id=document_id,
        level=level,
        text=text
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


def create_classification(
        db: Session,
        *,
        video_id: Optional[int] = None,
        document_id: Optional[int] = None,
        tag: str,
        score: float
) -> models.Classification:
    """
    Crea una clasificación ligada a un vídeo o a un documento.
    Debe pasarse video_id o document_id.
    """
    c = models.Classification(
        video_id=video_id,
        document_id=document_id,
        tag=tag,
        score=score
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


def create_classifications(
        db: Session,
        video_id: int,
        tags: List[Tuple[str, float]],
) -> List[models.Classification]:
    """
    Crea varias clasificaciones para un vídeo.
    - video_id: ID del vídeo
    - tags: lista de tuplas (tag, score)
    Devuelve la lista de Classification creadas.
    """
    created = []
    for tag, score in tags:
        c = create_classification(
            db,
            video_id=video_id,
            document_id=None,
            tag=tag,
            score=score
        )
        created.append(c)
    return created
