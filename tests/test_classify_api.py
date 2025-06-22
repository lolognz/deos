import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def patch_classifier(monkeypatch):
    # Patchea la función de servicio para no depender del modelo real
    monkeypatch.setattr(
        "app.services.classifier.classify_text",
        lambda text, top_k, threshold: [
                                           {"tag": "finanzas", "score": 0.9},
                                           {"tag": "educación", "score": 0.5},
                                       ][:top_k]
    )


def test_classify_endpoint_success():
    payload = {"text": "Hablemos de inversión y escuela", "top_k": 2, "threshold": 0.1}
    resp = client.post("/classify", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "tags" in data
    assert isinstance(data["tags"], list)
    assert data["tags"][0]["tag"] == "finanzas"
    assert data["tags"][1]["tag"] == "educación"


def test_classify_endpoint_missing_text():
    # Text es obligatorio → 422 Unprocessable Entity
    resp = client.post("/classify", json={"top_k": 2})
    assert resp.status_code == 422


def test_classify_endpoint_threshold_filtering():
    # threshold alto debería vaciar la lista
    # Usa el real para este caso
    resp = client.post("/classify", json={
        "text": "Invertir en bolsa",
        "top_k": 5,
        "threshold": 1.0
    })
    assert resp.status_code == 200
    assert resp.json()["tags"] == []
