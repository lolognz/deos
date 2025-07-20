import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.api.videos import get_db
from app.db import models
from app.db.session import Base
from app.main import app

# 1) Base de datos en memoria compartida
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# crear todas las tablas UNA vez
Base.metadata.create_all(bind=engine)


# 2) Fixture para poblar datos de ejemplo en cada módulo
@pytest.fixture(scope="module")
def db_setup():
    db = TestSessionLocal()

    # Vídeo 1
    v1 = models.Video(
        url="https://yt1", title="Video Uno", duration=60, topic="t1"
    )
    db.add(v1);
    db.commit();
    db.refresh(v1)
    db.add(models.Audio(video_id=v1.id, path="/a1.mp3"))
    db.add(models.Transcript(video_id=v1.id, text="Texto uno"))
    db.add(models.Summary(video_id=v1.id, level="short", text="Res1"))
    db.add(models.Classification(video_id=v1.id, tag="tecnología", score=0.9))

    # Vídeo 2
    v2 = models.Video(
        url="https://yt2", title="Video Dos", duration=120, topic="t2"
    )
    db.add(v2);
    db.commit();
    db.refresh(v2)
    db.add(models.Audio(video_id=v2.id, path="/a2.mp3"))
    db.add(models.Transcript(video_id=v2.id, text="Texto dos"))
    db.add(models.Summary(video_id=v2.id, level="short", text="Res2"))
    db.add(models.Classification(video_id=v2.id, tag="salud", score=0.8))

    db.commit()
    yield db
    db.close()


# 3) Override de la dependencia get_db en FastAPI
def override_get_db():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# 4) TestClient de FastAPI
client = TestClient(app)


# ——— Tests de integración ———

def test_list_videos_basic(db_setup):
    """GET /videos sin filtros devuelve los 2 vídeos insertados."""
    resp = client.get("/videos?skip=0&limit=10")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_video_detail(db_setup):
    """GET /videos/1 devuelve detalle completo, incluyendo sub-esquemas."""
    resp = client.get("/videos/1")
    assert resp.status_code == 200
    v = resp.json()
    assert v["id"] == 1
    assert v["url"] == "https://yt1"
    assert v["title"] == "Video Uno"
    assert "audio" in v and v["audio"]["path"] == "/a1.mp3"
    assert "transcript" in v and v["transcript"]["text"] == "Texto uno"
    assert "summary" in v and v["summary"]["text"] == "Res1"
    assert "classifications" in v
    # Debe tener al menos una clasificación y la primera es 'tecnología'
    assert any(c["tag"] == "tecnología" for c in v["classifications"])


def test_get_video_not_found(db_setup):
    """GET /videos/9999 devuelve 404 si no existe."""
    resp = client.get("/videos/9999")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Video not found"}


def test_filter_by_topic(db_setup):
    """GET /videos?topic=t1 devuelve solo el vídeo con topic 't1'."""
    resp = client.get("/videos?topic=t1")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["topic"] == "t1"


def test_filter_by_tag(db_setup):
    """GET /videos?tag=salud devuelve solo los vídeos clasificados como 'salud'."""
    resp = client.get("/videos?tag=salud")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["id"] == 2


def test_filter_by_date_range(db_setup):
    """
    GET /videos?date_from=<fecha> filtra por created_at >= date_from.
    Usamos la fecha de creación del vídeo 1 para asegurarnos de que
    al menos aparece ese registro.
    """
    # Sacamos created_at del primer vídeo
    first_video = db_setup.get(models.Video, 1)
    date_from = first_video.created_at.isoformat()
    resp = client.get(f"/videos?date_from={date_from}")
    assert resp.status_code == 200
    data = resp.json()
    # Debe incluir al menos el vídeo 1
    assert any(v["id"] == 1 for v in data)
