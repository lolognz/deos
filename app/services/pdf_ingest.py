# app/services/pdf_ingest.py
import fitz  # PyMuPDF
from fastapi import HTTPException


def extract_text_from_pdf_bytes(content: bytes) -> str:
    """
    Extrae el texto de un PDF en memoria.
    """
    try:
        doc = fitz.open(stream=content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        # HTTPException aquí sólo para que suba el status en la capa superior
        raise HTTPException(status_code=500, detail=f"Error extrayendo texto del PDF: {e}")
