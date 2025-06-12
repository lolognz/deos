# app/services/summarization.py
from typing import List

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# --- Configura aquí tu modelo; puedes probar con "t5-small" si tu máquina es modesta
MODEL_NAME = "facebook/bart-large-cnn"

_TOKENIZER = None
_MODEL = None
_MAX_INPUT_TOKENS = 1024  # límite típico de estos modelos


def _init_model():
    global _TOKENIZER, _MODEL
    if _MODEL is None or _TOKENIZER is None:
        _TOKENIZER = AutoTokenizer.from_pretrained(MODEL_NAME)
        _MODEL = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def _chunk_by_tokens(text: str, max_tokens: int) -> List[str]:
    _init_model()
    # Tokenizamos y contamos tokens correctamente
    tok = _TOKENIZER(text, return_tensors="pt")
    # tok["input_ids"] es un tensor shape (1, seq_len)
    seq_len = tok["input_ids"].shape[1]
    if seq_len <= max_tokens:
        return [text]
    # Si hace falta fragmentar
    import re
    sentences = re.split(r'(?<=[\.\?\!])\s+', text)
    chunks, current, current_count = [], [], 0
    for sent in sentences:
        sent_tok = _TOKENIZER(sent, return_tensors="pt")["input_ids"].shape[1]
        if current_count + sent_tok > max_tokens:
            chunks.append(" ".join(current))
            current, current_count = [sent], sent_tok
        else:
            current.append(sent)
            current_count += sent_tok
    if current:
        chunks.append(" ".join(current))
    return chunks


def summarize_text(text: str, level: str = "medium") -> str:
    """
    Resumen real con BART-CNN (o T5):
    - level: "short", "medium", "detailed" ajusta min/max tokens de salida.
    """
    _init_model()

    # Ajusta rangos de tokens de salida
    if level == "short":
        min_len, max_len = 20, 60
    elif level == "detailed":
        min_len, max_len = 100, 300
    else:
        min_len, max_len = 60, 150

    device = 0 if torch.cuda.is_available() else -1
    chunks = _chunk_by_tokens(text, _MAX_INPUT_TOKENS)

    summaries = []
    for chunk in chunks:
        inputs = _TOKENIZER(
            chunk, return_tensors="pt", truncation=True,
            max_length=_MAX_INPUT_TOKENS
        )
        if device >= 0:
            inputs = {k: v.to(device) for k, v in inputs.items()}
            _MODEL.to(device)
        # Generación con beam search para mayor coherencia
        summary_ids = _MODEL.generate(
            inputs["input_ids"],
            num_beams=4,
            length_penalty=2.0,
            min_length=min_len,
            max_length=max_len,
            early_stopping=True,
            no_repeat_ngram_size=3,
        )
        summary = _TOKENIZER.decode(
            summary_ids[0], skip_special_tokens=True
        ).strip()
        summaries.append(summary)

    # Si hemos tenido varios trozos, hacemos un último pase
    if len(summaries) > 1:
        combined = " ".join(summaries)
        # volver a resumir combined si es muy largo
        if len(_TOKENIZER(combined)["input_ids"]) > max_len:
            inputs = _TOKENIZER(
                combined, return_tensors="pt", truncation=True,
                max_length=_MAX_INPUT_TOKENS
            )
            summary_ids = _MODEL.generate(
                inputs["input_ids"],
                num_beams=4,
                length_penalty=2.0,
                min_length=min_len,
                max_length=max_len,
                early_stopping=True,
                no_repeat_ngram_size=3,
            )
            combined = _TOKENIZER.decode(
                summary_ids[0], skip_special_tokens=True
            ).strip()
        return combined

    return summaries[0]
