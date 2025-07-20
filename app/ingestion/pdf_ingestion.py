import pdfplumber
from sqlalchemy.orm import Session

from app.db import models


class PDFIngestor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text = ""

    def extract_text(self):
        """
        Extrae el texto de un archivo PDF.
        """
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                # Concatenamos el texto de todas las páginas
                self.text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
            return self.text
        except Exception as e:
            raise ValueError(f"Error al procesar el archivo PDF: {str(e)}")

    def save_to_db(self, db: Session, title: str):
        """
        Guarda el texto extraído del PDF en la base de datos.
        """
        if not self.text:
            raise ValueError("No se ha extraído texto del PDF")

        # Crear un nuevo registro de 'documento' en la base de datos
        document = models.Document(
            title=title,
            content=self.text
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        return document
