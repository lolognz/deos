from app.services.summarization import summarize_text


def test_summarize_text_short_returns_substring():
    text = " ".join(f"w{i}" for i in range(200))
    summary = summarize_text(text, level="short")
    assert isinstance(summary, str)
    # Debe ser más corto que el texto original pero no vacío
    assert 0 < len(summary) < len(text)


def test_summarize_text_medium_returns_substring():
    text = " ".join(f"w{i}" for i in range(50))
    summary = summarize_text(text, level="medium")
    assert isinstance(summary, str)
    # Cuando el texto es muy corto, retorno completo
    assert summary == text


def test_summarize_text_detailed_returns_substring():
    text = " ".join(f"w{i}" for i in range(500))
    summary = summarize_text(text, level="detailed")
    assert isinstance(summary, str)
    assert 0 < len(summary) < len(text)
