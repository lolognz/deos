import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import crud
from app.db.session import Base

# Base de datos en memoria para tests
SQLALCHEMY_TEST_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_and_get_video(db_session):
    url = "https://youtu.be/test"
    v = crud.create_video(db_session, url, "Título", 42, "topic")
    assert v.id is not None
    fetched = crud.get_video_by_url(db_session, url)
    assert fetched.id == v.id
    assert fetched.title == "Título"


def test_create_related_records(db_session):
    v = crud.create_video(db_session, "u", "t", 1, "x")
    a = crud.create_audio(db_session, v.id, "/path.mp3")
    t = crud.create_transcript(db_session, v.id, "texto")
    s = crud.create_summary(
        db_session,
        video_id=v.id,
        level="short",
        text="res"
    )
    cls = crud.create_classifications(db_session, v.id, [("tag1", 0.9), ("tag2", 0.5)])
    assert a.video_id == v.id
    assert t.video_id == v.id
    assert s.video_id == v.id
    assert len(cls) == 2
