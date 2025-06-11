import pytest

from app.services.transcriber import transcribe_audio


@pytest.fixture(autouse=True)
def patch_whisper_model(monkeypatch):
    """
    Este fixture intercepta whisper.load_model para devolver un modelo
    simulado cuya .transcribe() siempre retorna {"text": ""}.
    Así evitamos llamadas reales a ffmpeg.
    """

    class FakeModel:
        def transcribe(self, path):
            return {"text": ""}

    def fake_load_model(name):
        return FakeModel()

    # Parchea la función load_model de whisper
    monkeypatch.setattr("whisper.load_model", fake_load_model)


def test_transcribe_dummy(tmp_path):
    # Crea un "dummy.wav" vacío, pero no importará porque el modelo es fake
    dummy = tmp_path / "dummy.wav"
    dummy.write_bytes(b"")

    # Ahora transcribe_audio usará el FakeModel y no fallará con ffmpeg
    text = transcribe_audio(str(dummy))

    assert isinstance(text, str)
    assert text == ""
