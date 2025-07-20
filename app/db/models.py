from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, DateTime, Text, Float, ForeignKey, func
)
from sqlalchemy.orm import relationship

from app.db.session import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    topic = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relaciones 1:1
    audio = relationship("Audio", back_populates="video", uselist=False)
    transcript = relationship("Transcript", back_populates="video", uselist=False)
    summary = relationship("Summary", back_populates="video", uselist=False)

    # relación 1:N
    classifications = relationship("Classification", back_populates="video")


class Audio(Base):
    __tablename__ = "audios"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    video = relationship("Video", back_populates="audio")


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    video = relationship("Video", back_populates="transcript")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, index=True, nullable=False)
    topic = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # 1:N
    summaries = relationship("Summary", back_populates="document")
    classifications = relationship("Classification", back_populates="document")


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    level = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # ambos extremos
    video = relationship("Video", back_populates="summary")
    document = relationship("Document", back_populates="summaries")


class Classification(Base):
    __tablename__ = "classifications"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    tag = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # ambos extremos
    video = relationship("Video", back_populates="classifications")
    document = relationship("Document", back_populates="classifications")
