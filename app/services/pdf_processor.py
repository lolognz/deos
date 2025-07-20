from typing import Dict, Any, List

import fitz  # PyMuPDF
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db import crud
from app.db.session import SessionLocal
from app.services.classifier import classify_text
from app.services.summarization import summarize_text


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extrae el texto de un archivo PDF dado su path en disco.
    """
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el PDF: {e}")


def process_pdf_file(
        file_path: str,
        topic: str,
        summary_level: str
) -> Dict[str, Any]:
    """
    Orquesta la ingesta de un PDF completo:
      1) Extraer texto
      2) Generar resumen
      3) Clasificar
      4) Persistir en BD (documentos, resúmenes, clasificaciones)
    Devuelve un dict con los resultados.
    """
    # 1) Extraer texto
    text = extract_text_from_pdf(file_path)

    # 2) Generar resumen
    summary = summarize_text(text, level=summary_level)

    # 3) Clasificar texto resumido
    tags: List[Dict[str, Any]] = classify_text(
        summary, top_k=3, threshold=0.2
    )

    # 4) Persistir en la base de datos
    db: Session = SessionLocal()
    try:
        # 4.1) Crear o recuperar registro de documento
        doc = crud.get_document_by_path(db, file_path)
        if not doc:
            doc = crud.create_document(db, path=file_path, topic=topic)

        # 4.2) Crear resumen asociado al documento
        crud.create_summary(
            db,
            video_id=None,
            document_id=doc.id,
            level=summary_level,
            text=summary
        )

        # 4.3) Crear cada clasificación asociada
        for tag_info in tags:
            crud.create_classification(
                db,
                video_id=None,
                document_id=doc.id,
                tag=tag_info["tag"],
                score=tag_info["score"]
            )

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    return {
        "file_path": file_path,
        "topic": topic,
        "summary": summary,
        "tags": tags,
    }
