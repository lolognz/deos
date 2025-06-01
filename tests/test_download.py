import os
from modules.downloader import download


def test_download_audio():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    filename, title, duration, webpage_url = download.download_audio_from_youtube(url)

    assert os.path.exists(filename)
    assert filename.endswith(".mp3")
    assert title is not None
    assert duration > 0
    assert "youtube.com" in webpage_url

    # Limpieza del archivo descargado tras test
    os.remove(filename)
