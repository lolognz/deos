# app/services/transcriber.py
import os

# Quitamos la carga inmediata:
# MODEL = whisper.load_model("base")

# Usamos un contenedor para el modelo
_MODEL = None

# Configurar variables de entorno para evitar warnings
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")


def transcribe_audio(path: str) -> tuple[str, float]:
    """
    Carga el modelo Whisper la primera vez que se invoca y luego transcribe.
    Devuelve (texto_transcrito, duracion_en_segundos)
    """
    global _MODEL
    if _MODEL is None:
        import whisper
        _MODEL = whisper.load_model("base")

    if not os.path.isfile(path):
        raise FileNotFoundError(f"No existe el archivo de audio: {path}")

    result = _MODEL.transcribe(path)
    text = result.get("text", "").strip()
    duration = result.get("duration", 0.0)
    
    return text, duration
