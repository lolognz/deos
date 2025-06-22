from app.services.classifier import classify_text


def test_classify_text_basic_top2():
    text = "Vamos a hablar de bolsa, acciones e inversión en el mercado financiero."
    tags = classify_text(text, top_k=2, threshold=0.1)
    # Debe devolver las 2 más relevantes: finanzas primero
    assert tags[0]["tag"] == "finanzas"
    assert tags[0]["score"] > tags[1]["score"]
    assert len(tags) == 2


def test_classify_text_threshold_filters_out():
    text = "Un tema totalmente ajeno, mención a nada de nuestros temas."
    tags = classify_text(text, top_k=5, threshold=0.5)
    # Ningún tema alcanza threshold alto
    assert tags == []


def test_classify_text_threshold_lower_than_score():
    """
    Test para comprobar que el sistema filtra correctamente cuando el threshold
    es mayor que el score de todas las etiquetas.
    """
    text = "Una mención pequeña sobre finanzas"
    tags = classify_text(text, top_k=5, threshold=0.8)
    # No debe devolver ninguna etiqueta porque el score de finanzas es menor que el threshold
    assert tags == []


def test_classify_text_top_k_larger_than_available():
    """
    Test para verificar que si se pide más etiquetas de las disponibles,
    el sistema devuelve solo las etiquetas existentes.
    """
    text = "La salud y bienestar en tiempos de pandemia"
    tags = classify_text(text, top_k=10, threshold=0.1)
    # No puede devolver más de las etiquetas disponibles (asumimos que hay menos de 10)
    assert len(tags) <= 5  # Suponiendo que no haya más de 5 etiquetas disponibles


def test_classify_text_empty_text():
    """
    Test para verificar que el sistema maneja correctamente un texto vacío.
    """
    text = ""
    tags = classify_text(text, top_k=3, threshold=0.1)
    # No debe devolver ninguna etiqueta
    assert tags == []


def test_classify_text_single_word():
    """
    Test para verificar que el sistema maneja correctamente un texto muy corto (una sola palabra).
    """
    text = "salud"
    tags = classify_text(text, top_k=3, threshold=0.1)
    # La primera etiqueta debe ser 'salud'
    assert tags[0]["tag"] == "salud"
    # No devolvemos más de top_k etiquetas
    assert len(tags) <= 3
    # Cada score debe ser >= threshold
    assert all(t["score"] >= 0.1 for t in tags)


def test_classify_text_multiple_languages():
    """
    Test para comprobar cómo el sistema maneja un texto que contiene varios idiomas.
    """
    text = "La inteligencia artificial está cambiando el mundo. AI is the future."
    tags = classify_text(text, top_k=3, threshold=0.1)
    # Debería devolver etiquetas que incluyan "tecnología" o similar
    assert "tecnología" in [tag["tag"] for tag in tags]
