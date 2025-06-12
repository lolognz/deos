from typing import List

from pydantic import BaseModel, HttpUrl


class YouTubeRequest(BaseModel):
    url: HttpUrl


class BulkYouTubeRequest(BaseModel):
    urls: List[HttpUrl]


class SummarizeRequest(BaseModel):
    text: str
    level: str = "medium"
