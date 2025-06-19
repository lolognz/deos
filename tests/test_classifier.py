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
