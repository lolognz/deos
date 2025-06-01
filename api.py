from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from modules.downloader import download

app = FastAPI()


class YouTubeURL(BaseModel):
    url: str


@app.post("/download-audio")
async def download_audio_endpoint(data: YouTubeURL):
    try:
        filename, title, duration, page_url = download.download_audio_from_youtube(data.url)
        return {
            "filename": filename,
            "title": title,
            "duration": duration,
            "url": page_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
