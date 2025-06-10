import os

import pytest

from app.core.config import settings
from app.services.downloader import download_audio_from_youtube


@pytest.fixture()
def cleanup_download_dir(tmp_path, monkeypatch):
    # Override download_dir in settings to tmp_path
    monkeypatch.setenv('DOWNLOAD_DIR', str(tmp_path))
    settings.download_dir = str(tmp_path)
    return tmp_path


@pytest.fixture(autouse=True)
def patch_youtubedl(monkeypatch):
    # monkeypatch YoutubeDL.extract_info to avoid network calls
    from yt_dlp import YoutubeDL
    def fake_extract_info(self, url, download):
        # Simulate extract_info and create dummy file
        info = {'id': 'test123', 'title': 'Test Title', 'duration': 42, 'webpage_url': url}
        # write dummy mp3 to settings.download_dir
        from app.core.config import settings
        os.makedirs(settings.download_dir, exist_ok=True)
        dummy_path = os.path.join(settings.download_dir, f"{info['id']}.mp3")
        with open(dummy_path, 'wb') as f:
            f.write(b'test')
        return info

    monkeypatch.setattr(YoutubeDL, 'extract_info', fake_extract_info)


def test_download_audio_success(cleanup_download_dir):
    # Act
    path, title, duration, page_url = download_audio_from_youtube(
        youtube_url="https://youtu.be/dQw4w9WgXcQ"
    )

    # Assert
    assert title == 'Test Title'
    assert duration == 42
    assert page_url == "https://youtu.be/dQw4w9WgXcQ"
    assert path.endswith('test123.mp3')
    assert os.path.exists(path)
