# app/services/transcriber.py
import os

# Quitamos la carga inmediata:
# MODEL = whisper.load_model("base")

# Usamos un contenedor para el modelo
_MODEL = None


def transcribe_audio(path: str) -> str:
    """
    Carga el modelo Whisper la primera vez que se invoca y luego transcribe.
    """
    global _MODEL
    if _MODEL is None:
        import whisper
        _MODEL = whisper.load_model("base")

    if not os.path.isfile(path):
        raise FileNotFoundError(f"No existe el archivo de audio: {path}")

    result = _MODEL.transcribe(path)
    return result.get("text", "").strip()
