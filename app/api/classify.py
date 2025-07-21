from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.classifier import classify_text

router = APIRouter(prefix="", tags=["classification"])


class ClassifyRequest(BaseModel):
    text: str = Field(..., json_schema_extra={"example": "Texto a clasificar"})
    top_k: Optional[int] = Field(3, ge=1, json_schema_extra={"example": 3})
    threshold: Optional[float] = Field(0.0, ge=0, le=1, json_schema_extra={"example": 0.3})


class TagScore(BaseModel):
    tag: str
    score: float


class ClassifyResponse(BaseModel):
    tags: List[TagScore]


@router.post("/classify", response_model=ClassifyResponse)
async def classify_endpoint(req: ClassifyRequest):
    """
    Clasifica el texto y devuelve hasta top_k etiquetas con score >= threshold.
    """
    try:
        tags = classify_text(
            text=req.text,
            top_k=req.top_k,
            threshold=req.threshold
        )
        return ClassifyResponse(tags=tags)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
