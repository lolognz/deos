import os

from yt_dlp import YoutubeDL

from app.core.config import settings


def download_audio_from_youtube(youtube_url: str):
    if not isinstance(youtube_url, str):
        raise ValueError("download_audio_from_youtube requiere un string como URL")
    os.makedirs(settings.download_dir, exist_ok=True)
    opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{settings.download_dir}/%(id)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True,
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = os.path.join(settings.download_dir, f"{info['id']}.mp3")
    return filename, info.get("title"), info.get("duration"), info.get("webpage_url")
