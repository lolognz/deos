from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# Asegúrate de tener python-multipart instalado para FastAPI File

def test_ingest_pdf_endpoint(tmp_path, monkeypatch):
    """
    Prueba el endpoint POST /ingest/pdf subiendo un fichero PDF.
    """
    # 1) Creamos un PDF muy sencillo en tmp_path
    pdf_path = tmp_path / "test.pdf"
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(str(pdf_path))
    c.drawString(50, 800, "Texto de prueba para API")
    c.save()

    # 2) Llamamos al endpoint
    with open(pdf_path, "rb") as f:
        response = client.post(
            "/ingest/pdf",
            files={"file": ("test.pdf", f, "application/pdf")},
            data={"topic": "t_api", "level": "short"}
        )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["file_path"].endswith("test.pdf")
    assert data["topic"] == "t_api"
    assert "summary" in data
    assert isinstance(data["tags"], list)
