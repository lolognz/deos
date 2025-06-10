import logging

from fastapi import APIRouter, HTTPException
from fastapi import BackgroundTasks

from app.models.request_models import BulkYouTubeRequest
from app.models.request_models import YouTubeRequest
from app.services.downloader import download_audio_from_youtube

router = APIRouter()
log = logging.getLogger(__name__)


@router.post("/download")
async def download_audio(req: YouTubeRequest):
    url_str = str(req.url)  # <<< convierto a str
    log.info(f"Recibida petición para descargar: {url_str}")
    try:
        filename, title, duration, page_url = download_audio_from_youtube(url_str)
        return {
            "path": filename,
            "title": title,
            "duration": duration,
            "url": page_url
        }
    except Exception as e:
        log.exception("Error en descarga de audio")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/download/bulk")
async def download_bulk(
        req: BulkYouTubeRequest,
        background_tasks: BackgroundTasks
):
    """
    Recibe { "urls": [lista de HttpUrl] } y encola la descarga de cada URL.
    """
    tasks = []
    for url in req.urls:
        url_str = str(url)
        background_tasks.add_task(download_audio_from_youtube, url_str)
        tasks.append({"url": url_str, "status": "queued"})
    return {"tasks": tasks}
