from typing import Optional, Dict

from app.services.classifier import classify_text
from app.services.downloader import download_audio_from_youtube
from app.services.summarization import summarize_text
from app.services.transcriber import transcribe_audio


def process_audio_url(
        youtube_url: str,
        topic: Optional[str] = None,
        summary_level: str = "medium"
) -> Dict[str, Optional[str]]:
    """
    Orquesta todo el pipeline para una URL de YouTube:
      1) Descarga el audio
      2) Transcribe a texto
      3) Resume el texto
      4) Adjunta el tema si se proporcionó

    Params:
    - youtube_url: URL del video de YouTube a procesar.
    - topic:       Etiqueta temática opcional asociada al contenido.
    - summary_level: Nivel de detalle del resumen: "short", "medium" o "detailed".

    Returns:
    Un diccionario con:
    {
      "url":          <youtube_url>,
      "audio_path":   <ruta local al mp3>,
      "transcript":   <texto completo transcrito>,
      "summary":      <resumen generado>,
      "topic":        <topic o None>
    }
    """
    # 1) Descargar audio y obtener metadatos básicos
    audio_path, title, duration, page_url = download_audio_from_youtube(youtube_url)

    # 2) Transcribir el archivo MP3 a texto
    transcript = transcribe_audio(audio_path)

    # 3) Generar un resumen a partir de la transcripción
    summary = summarize_text(transcript, level=summary_level)

    # 4) Clasificar por temática
    tags = classify_text(summary, top_k=3, threshold=0.2)

    # 5) Construir y devolver el objeto de resultado
    return {
        "url": youtube_url,
        "audio_path": audio_path,
        "title": title,
        "duration": duration,
        "transcript": transcript,
        "summary": summary,
        "topic": topic,
        "tags": tags,
    }
