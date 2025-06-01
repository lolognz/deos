from modules.downloader import download

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Ashley - never gonna give you up
filename, title, duration, page_url = download.download_audio_from_youtube(url)

print(f"✅ Archivo guardado en: {filename}")
print(f"🎵 Título: {title}")
print(f"⏱ Duración: {duration} segundos")
print(f"🔗 URL: {page_url}")
