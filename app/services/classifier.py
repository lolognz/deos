from typing import List, Dict, Any

from sentence_transformers import SentenceTransformer, util

# Definimos las temáticas con sus descripciones
THEMES: Dict[str, str] = {
    "tecnología": (
        "inteligencia artificial, software, hardware, programación, "
        "artificial intelligence, software, hardware, programming"
    ),
    "salud": (
        "medicina, enfermedad, tratamiento, clínica, hospital, "
        "medicine, disease, treatment, clinic, hospital"
    ),
    "educación": (
        "enseñanza, alumnos, escuela, universidad, aprendizaje, "
        "teaching, students, school, university, learning"
    ),
    "finanzas": (
        "inversión, mercado, acciones, economía, bolsa, "
        "investment, market, stocks, economy, finance"
    ),
    "deporte": (
        "fútbol, baloncesto, tenis, competición, atleta, "
        "football, basketball, tennis, competition, athlete"
    ),
}

# Cargamos un modelo ligero de embeddings
_MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def classify_text(
        text: str,
        top_k: int = 3,
        threshold: float = 0.0
) -> List[Dict[str, Any]]:
    """
    Clasifica el texto en las temáticas más relevantes.

    Params:
    - text:      Texto a clasificar.
    - top_k:     Máximo número de etiquetas a devolver.
    - threshold: Minimín de similitud coseno para incluir una etiqueta.

    Returns:
    - Una lista de dicts { tag: str, score: float }, ordenada por score descendente.
    """
    # 1) Embedding del texto
    text_emb = _MODEL.encode(text, convert_to_tensor=True)

    # 2) Embeddings de las descripciones
    theme_names = list(THEMES.keys())
    theme_descs = list(THEMES.values())
    theme_embs = _MODEL.encode(theme_descs, convert_to_tensor=True)

    # 3) Cálculo de similitud coseno
    sims = util.cos_sim(text_emb, theme_embs)[0]  # tensor shape (num_themes,)

    # 4) Empaquetar con nombres y scores
    pairs = [(theme_names[i], float(sims[i])) for i in range(len(theme_names))]

    # 5) Filtrar por threshold y ordenar por score
    filtered = [{"tag": tag, "score": score}
                for tag, score in pairs if score >= threshold]
    filtered.sort(key=lambda x: x["score"], reverse=True)

    # 6) Devolver sólo top_k
    return filtered[:top_k]
