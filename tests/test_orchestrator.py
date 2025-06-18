from unittest.mock import patch

import pytest

from app.services.orchestrator import process_audio_url


# Fixture para sustituir las funciones reales por mocks
@pytest.fixture
def patch_services(monkeypatch):
    # Mock de download_audio_from_youtube
    def mock_download_audio(url):
        return (
            "/ruta/falsa/audio.mp3",  # audio_path
            "Título falso",  # title
            123,  # duration
            "https://url.falsa.com"  # page_url
        )

    monkeypatch.setattr("app.services.orchestrator.download_audio_from_youtube", mock_download_audio)

    # Mock de transcribe_audio
    def mock_transcribe(audio_path):
        return ("Texto transcrito falso", 123)

    monkeypatch.setattr("app.services.orchestrator.transcribe_audio", mock_transcribe)

    # Mock de summarize_text
    def mock_summarize(text, topic=None, level="short"):
        return "Resumen falso"

    monkeypatch.setattr("app.services.orchestrator.summarize_text", mock_summarize)


def test_process_audio_url(patch_services):
    url = "https://youtube.com/watch?v=fake"
    result = process_audio_url(url, topic="test_topic", summary_level="short")

    # Ya no existe 'title' directo, no hacemos ese assert
    assert result["url"] == url
    assert result["audio_path"] == "/ruta/falsa/audio.mp3"

    # transcript es una tupla: (texto, duración)
    transcript_text, duration = result["transcript"]
    assert transcript_text == "Texto transcrito falso"
    assert duration == 123

    assert result["summary"] == "Resumen falso"
    assert result["topic"] == "test_topic"


@pytest.mark.integration
@patch("app.services.orchestrator.download_audio_from_youtube")
@patch("app.services.orchestrator.transcribe_audio")
@patch("app.services.orchestrator.summarize_text")
def test_process_audio_url_integration_with_mocks(
        mock_summarize,
        mock_transcribe,
        mock_download_audio
):
    # Configuramos los mocks para devolver datos simulados
    mock_download_audio.return_value = (
        "/fake/path/audio.mp3",
        "Mock Title",
        123,
        "https://youtube.com/watch?v=mock"
    )
    mock_transcribe.return_value = ("Mock transcript text", 123)
    mock_summarize.return_value = "Mock summary text"

    url = "https://youtube.com/watch?v=mock"
    result = process_audio_url(url, topic="integration_mock", summary_level="short")

    print(result)  # Para depurar si quieres

    assert result["audio_path"] == "/fake/path/audio.mp3"
    assert result["title"] == "Mock Title"
    transcript_text, duration = result["transcript"]
    assert transcript_text == "Mock transcript text"
    assert duration == 123
    assert result["summary"] == "Mock summary text"
    assert result["topic"] == "integration_mock"
    assert result["url"] == url
