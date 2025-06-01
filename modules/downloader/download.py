# audio_extraction/download.py
from yt_dlp import YoutubeDL
import os


def download_audio_from_youtube(youtube_url, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = os.path.join(output_dir, f"{info['id']}.mp3")
        return filename, info.get('title'), info.get('duration'), info.get('webpage_url')
