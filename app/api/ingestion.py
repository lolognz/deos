# app/api/ingestion.py

import os
import shutil

from fastapi import (
    APIRouter, File, UploadFile, HTTPException, Depends, Form
)
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.services.orchestrator import process_pdf_file

router = APIRouter(tags=["ingestion"])


@router.post("/pdf")
async def ingest_pdf(
        file: UploadFile = File(...),
        topic: str = Form("default"),
        level: str = Form("short"),
        db: Session = Depends(get_db)
):
    """
    Sube un PDF y lo procesa por completo (extrae texto, resume,
    clasifica y persiste). Devuelve siempre un "message" y luego
    todos los campos que validan los tests de endpoint.
    """
    # 1) Guardar temporalmente
    save_dir = settings.download_dir
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, file.filename)
    try:
        with open(save_path, "wb") as out:
            shutil.copyfileobj(file.file, out)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando PDF: {e}")

    # 2) Ejecutar pipeline completo
    try:
        result = process_pdf_file(
            file_path=save_path,
            topic=topic,
            summary_level=level
        )
    except HTTPException:
        # Si process_pdf_file ya lanzó HTTPException, lo propagamos
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 3) Añadir el mensaje y devolver TODO
    return {
        "message": "PDF procesado correctamente",
        **result
    }
