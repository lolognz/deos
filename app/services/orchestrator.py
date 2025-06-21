# app/services/orchestrator.py

from typing import Dict, Any, List

# Importamos la sesión y los CRUDs
from sqlalchemy.orm import Session

from app.db import crud
from app.db.session import SessionLocal
from app.services.classifier import classify_text
# Importamos los servicios puros
from app.services.downloader import download_audio_from_youtube
from app.services.summarization import summarize_text
from app.services.transcriber import transcribe_audio


def process_audio_url(
        youtube_url: str,
        topic: str,
        summary_level: str
) -> Dict[str, Any]:
    """
    Orquesta todo el pipeline y persiste cada parte en la base de datos:

    1) Descargar audio
    2) Transcribir
    3) Resumir
    4) Clasificar
    5) Guardar en DB: videos, audios, transcripciones, resúmenes, clasificaciones

    Devuelve un dict con todos los datos procesados.
    """
    # -------------------------------------
    # 1) Descargar audio del vídeo
    # -------------------------------------
    audio_path, title, duration, page_url = download_audio_from_youtube(youtube_url)

    # -------------------------------------
    # 2) Transcribir el audio
    # -------------------------------------
    transcript_text, transcript_duration = transcribe_audio(audio_path)

    # -------------------------------------
    # 3) Generar resumen del texto
    # -------------------------------------
    summary = summarize_text(transcript_text, level=summary_level)

    # -------------------------------------
    # 4) Clasificar temática
    # -------------------------------------
    tags: List[Dict[str, Any]] = classify_text(
        summary,
        top_k=3,
        threshold=0.2
    )

    # -------------------------------------
    # 5) Persistencia en la base de datos
    # -------------------------------------
    db: Session = SessionLocal()
    try:
        # 5.1) Crear o recuperar el registro de vídeo
        video = crud.get_video_by_url(db, youtube_url)
        if not video:
            video = crud.create_video(
                db,
                url=youtube_url,
                title=title,
                duration=duration,
                topic=topic
            )

        # 5.2) Guardar Audio
        #    Solo si no existe ya uno para este vídeo (reemplaza si quieres)
        crud.create_audio(db, video_id=video.id, path=audio_path)

        # 5.3) Guardar Transcripción
        crud.create_transcript(db, video_id=video.id, text=transcript_text)

        # 5.4) Guardar Resumen
        crud.create_summary(
            db,
            video_id=video.id,
            level=summary_level,
            text=summary
        )

        # 5.5) Guardar cada etiqueta de clasificación
        for tag_info in tags:
            crud.create_classification(
                db,
                video_id=video.id,
                tag=tag_info["tag"],
                score=tag_info["score"]
            )

        # Confirmar todo
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    # -------------------------------------
    # 6) Construir y devolver el resultado
    # -------------------------------------
    result: Dict[str, Any] = {
        "url": youtube_url,
        "audio_path": audio_path,
        "title": title,
        "duration": duration,
        "transcript": (transcript_text, transcript_duration),
        "summary": summary,
        "topic": topic,
        "tags": tags,
    }
    return result
