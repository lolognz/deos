import os

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app

client = TestClient(app)

@pytest.fixture()
def setup_tmp_download_dir(monkeypatch, tmp_path):
    # Override download_dir in settings to tmp_path
    monkeypatch.setenv('DOWNLOAD_DIR', str(tmp_path))
    settings.download_dir = str(tmp_path)
    return tmp_path


def test_download_endpoint_success(monkeypatch, setup_tmp_download_dir):
    # Stub download_audio_from_youtube to avoid real download
    def fake_download(youtube_url: str):
        filename = os.path.join(settings.download_dir, 'abc.mp3')
        with open(filename, 'wb') as f:
            f.write(b'test')
        return filename, 'Fake Title', 10, youtube_url

    # parchear la función real en el servicio
    import app.services.downloader as downloader_module
    monkeypatch.setattr(downloader_module, 'download_audio_from_youtube', fake_download)

    # además patch en el router para asegurar uso del fake
    import app.api.audio as audio_module
    monkeypatch.setattr(audio_module, 'download_audio_from_youtube', fake_download)

    response = client.post(
        '/audio/download', json={'url': 'https://www.youtube.com/watch?v=test'}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 'Fake Title'
    assert data['duration'] == 10
    assert data['url'] == 'https://www.youtube.com/watch?v=test'
    assert data['path'].endswith('abc.mp3')


def test_summarize_endpoint_success(monkeypatch):
    # Stubea la función en el router, no en el servicio
    def fake_summary(text, level):
        assert text == "Hola mundo"
        assert level == "short"
        return "Hola…"

    import app.api.audio as audio_module
    monkeypatch.setattr(audio_module, 'summarize_text', fake_summary)

    response = client.post(
        '/audio/summarize',
        json={'text': 'Hola mundo', 'level': 'short'}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['summary'] == "Hola…"
