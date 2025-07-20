from typing import Dict, Any, List

from sqlalchemy.orm import Session

from app.db import crud
from app.db.session import SessionLocal
from app.services.classifier import classify_text
from app.services.downloader import download_audio_from_youtube
from app.services.summarization import summarize_text
from app.services.transcriber import transcribe_audio


def process_audio_url(
        youtube_url: str,
        topic: str,
        summary_level: str
) -> Dict[str, Any]:
    """
    Orquesta todo el pipeline para un video de YouTube:
    1) Descargar audio
    2) Transcribir
    3) Resumir
    4) Clasificar
    5) Persistir en BD (videos, audios, transcripciones, resúmenes, clasificaciones)
    Devuelve un dict con todos los datos procesados.
    """
    # 1) Descargar audio
    audio_path, title, duration, page_url = download_audio_from_youtube(youtube_url)

    # 2) Transcribir
    transcript_text, transcript_duration = transcribe_audio(audio_path)

    # 3) Resumir
    summary = summarize_text(transcript_text, level=summary_level)

    # 4) Clasificar
    tags: List[Dict[str, Any]] = classify_text(
        summary,
        top_k=3,
        threshold=0.2
    )

    # 5) Persistir en la base de datos
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

        # 5.2) Crear audio
        crud.create_audio(db, video_id=video.id, path=audio_path)

        # 5.3) Crear transcripción
        crud.create_transcript(db, video_id=video.id, text=transcript_text)

        # 5.4) Crear resumen
        crud.create_summary(
            db,
            video_id=video.id,
            level=summary_level,
            text=summary
        )

        # 5.5) Crear clasificaciones
        for tag_info in tags:
            crud.create_classification(
                db,
                video_id=video.id,
                tag=tag_info["tag"],
                score=tag_info["score"]
            )

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    # 6) Construir y devolver el resultado
    return {
        "url": youtube_url,
        "audio_path": audio_path,
        "title": title,
        "duration": duration,
        "transcript": (transcript_text, transcript_duration),
        "summary": summary,
        "topic": topic,
        "tags": tags,
    }


def process_pdf_file(
        file_path: str,
        topic: str,
        summary_level: str
) -> Dict[str, Any]:
    """
    Orquesta la ingesta de un PDF:
      1) Extraer texto
      2) Resumir
      3) Clasificar
      4) Persistir en BD
    Devuelve un dict con todos los resultados.
    """
    # 1) Extraer texto
    with open(file_path, "rb") as f:
        content = f.read()
    # Importamos aquí para evitar circularidades
    from app.services import pdf_ingest
    extracted_text = pdf_ingest.extract_text_from_pdf_bytes(content)

    # 2) Resumir
    summary = summarize_text(extracted_text, level=summary_level)

    # 3) Clasificar
    tags: List[Dict[str, Any]] = classify_text(
        summary, top_k=3, threshold=0.2
    )

    # 4) Persistir en BD
    db: Session = SessionLocal()
    try:
        doc = crud.get_document_by_path(db, file_path)
        if not doc:
            doc = crud.create_document(db, path=file_path, topic=topic)

        crud.create_summary(
            db,
            document_id=doc.id,
            level=summary_level,
            text=summary
        )
        for tag in tags:
            crud.create_classification(
                db,
                document_id=doc.id,
                tag=tag["tag"],
                score=tag["score"]
            )
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    # 5) Devolver todo lo que esperan los tests:
    return {
        "file_path": file_path,
        "topic": topic,
        "level": summary_level,
        "extracted_text": extracted_text,
        "summary": summary,
        "tags": tags,
    }
