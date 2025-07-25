import logging
import os
from typing import Tuple

from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


def download_audio_from_youtube(youtube_url: str) -> Tuple[str, str, int, str]:
    logger.info(f"Descargando audio de {youtube_url}")
    download_dir = os.getenv("DOWNLOAD_DIR", "data/downloads")
    os.makedirs(download_dir, exist_ok=True)
    out_template = os.path.join(download_dir, "%(id)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": out_template,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": True,
        "http_headers": {
            # User‑Agent típico de navegador moderno
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
                          "AppleWebKit/537.36 (KHTML, like Gecko) " +
                          "Chrome/120.0.0.0 Safari/537.36",
        },
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(youtube_url, download=True)
        except Exception as e:
            logger.error(f"Error descargando audio: {e}", exc_info=True)
            raise

    filename = ydl.prepare_filename(info)  # ruta al fichero descargado
    title = info.get("title")
    duration = info.get("duration")
    webpage_url = info.get("webpage_url")
    return filename, title, duration, webpage_url
