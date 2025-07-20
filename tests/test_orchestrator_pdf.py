import pytest
# Generamos un PDF mínimamente válido para la prueba
from reportlab.pdfgen import canvas

from app.services.pdf_processor import process_pdf_file


@pytest.fixture(scope="module")
def sample_pdf(tmp_path_factory):
    path = tmp_path_factory.mktemp("pdfs") / "sample.pdf"
    c = canvas.Canvas(str(path))
    c.drawString(100, 750, "Prueba de contenido PDF")
    c.save()
    return str(path)


def test_process_pdf_file_creates_and_returns(sample_pdf):
    """
    A partir de un PDF de ejemplo, process_pdf_file debe devolver
    un dict con file_path, topic, summary y tags.
    """
    result = process_pdf_file(
        file_path=sample_pdf,
        topic="test_topic",
        summary_level="short"
    )
    assert result["file_path"] == sample_pdf
    assert result["topic"] == "test_topic"
    assert "summary" in result and isinstance(result["summary"], str)
    assert "tags" in result and isinstance(result["tags"], list)
