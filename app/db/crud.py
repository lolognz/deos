from datetime import datetime
from typing import List, Tuple, Optional

from sqlalchemy.orm import Session

from app.db import models


def get_video_by_url(db: Session, url: str) -> models.Video:
    return db.query(models.Video).filter(models.Video.url == url).first()


def create_video(
        db: Session,
        url: str,
        title: str,
        duration: int,
        topic: str
) -> models.Video:
    video = models.Video(
        url=url, title=title, duration=duration, topic=topic
    )
    db.add(video)
    db.commit()
    db.refresh(video)
    return video


def create_audio(db: Session, video_id: int, path: str):
    audio = models.Audio(video_id=video_id, path=path)
    db.add(audio)
    db.commit()
    return audio


def create_transcript(db: Session, video_id: int, text: str):
    t = models.Transcript(video_id=video_id, text=text)
    db.add(t);
    db.commit();
    return t


def create_summary(db: Session, video_id: int, level: str, text: str):
    s = models.Summary(video_id=video_id, level=level, text=text)
    db.add(s);
    db.commit();
    return s


def create_classifications(db: Session, video_id: int, tags: List[Tuple[str, float]]):
    objs = [models.Classification(
        video_id=video_id, tag=tag, score=score
    ) for tag, score in tags]
    db.add_all(objs)
    db.commit()
    return objs


def create_classification(
        db: Session,
        video_id: int,
        tag: str,
        score: float
) -> models.Classification:
    """
    Crea un registro de clasificación para un vídeo.
    """
    cls = models.Classification(
        video_id=video_id,
        tag=tag,
        score=score
    )
    db.add(cls)
    db.commit()
    db.refresh(cls)
    return cls


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
    Devuelve una lista de Video, con paginación y filtros opcionales:
      - topic: exact match en Video.topic
      - tag:   join con Classification.tag
      - date_from/date_to: rango en Video.created_at
    """
    query = db.query(models.Video)

    # Filtrar por topic
    if topic:
        query = query.filter(models.Video.topic == topic)

    # Filtrar por rango de fechas
    if date_from:
        query = query.filter(models.Video.created_at >= date_from)
    if date_to:
        query = query.filter(models.Video.created_at <= date_to)

    # Filtrar por tag, haciendo JOIN con classifications
    if tag:
        query = query.join(models.Classification) \
            .filter(models.Classification.tag == tag) \
            .distinct()

    # Paginación
    videos = query.offset(skip).limit(limit).all()
    return videos


def get_video_by_id(db: Session, video_id: int) -> models.Video:
    """
    Devuelve un Video por su ID, o None si no existe.
    """
    return db.query(models.Video).filter(models.Video.id == video_id).first()
