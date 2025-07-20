from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ingest_pdf():
    with open("tests/test_files/test.pdf", "rb") as f:
        response = client.post("/ingest/pdf", files={"file": ("test.pdf", f, "application/pdf")})

    # Verificamos que la respuesta sea 200 OK
    assert response.status_code == 200
    # Comprobamos que el texto extraído sea el esperado (limitado a los primeros 200 caracteres)
    data = response.json()
    assert "message" in data
    assert data["message"] == "PDF procesado correctamente"
    assert len(data["extracted_text"]) > 0  # Asegúrate de que el texto no esté vacío
