DEOS Service
<div align="center"> <img src="https://raw.githubusercontent.com/tu-org/DEOS/main/docs/logo.png" alt="DEOS Logo" width="200"/> </div>
📖 Índice

    Descripción y Objetivos

    Funciones Principales

    Estado Actual vs. Pendientes

    Tecnologías y Dependencias

    Estructura del Proyecto

    Guía de Uso

        1. Instalación

        2. Configuración

        3. Ejecutar en Local

        4. Docker (opcional)

    API & Endpoints

        /audio/download

        /videos …

        /ingest/pdf

    Testing

        Unitarios

        Integración

        Colección Postman

    Buenas Prácticas

    Despliegue en Producción

        Estrategia CI/CD

        Entorno y Monitoreo

    Contribuir

    Licencia

📖 Descripción y Objetivos

DEOS (Deep Extraction, Orchestration & Summarization) es un microservicio desarrollado en FastAPI para:

    Descarga de audio desde URLs de YouTube.

    Transcripción de audio a texto (usando OpenAI Whisper).

    Resumen de transcripciones (múltiples niveles).

    Clasificación de resúmenes en etiquetas semánticas.

    Ingesta de PDFs: extracción de texto, resumen y clasificación.

    Persistencia en base de datos SQL (SQLite/PostgreSQL).

Objetivo final:
Crear un pipeline automatizado que permita a usuarios o sistemas terceros enviar un vídeo o PDF y obtener, de forma
RESTful, metadatos enriquecidos (transcripción, resumen, etiquetas) con trazabilidad en base de datos.
🔧 Funciones Principales
Función / Endpoint Pipeline
/audio/download 1. Descarga audio → 2. Transcribe → 3. Resume → 4. Clasifica → 5. Persiste registros en BD
/videos/list    (Pendiente) Listar vídeos procesados, con filtros y paginación
/audio/process-url Orquesta manual sin persistencia (útil para pruebas rápidas)
/ingest/pdf 1. Guarda PDF → 2. Extrae texto → 3. Resume → 4. Clasifica → 5. Persiste documento, resumen, etiquetas en BD
/classify/text    (Pendiente) Recibe texto y devuelve etiquetas sin almacenamiento
📋 Estado Actual vs. Pendientes
Tarea Estado
Descarga de audio con yt-dlp ✅ Completado
Transcripción con Whisper ✅ Completado
Resumen con Transformers ✅ Completado
Clasificación con Sentence‑Transformers ✅ Completado
Persistencia en BD SQLAlchemy ✅ Completado
Endpoint /audio/download ✅ Completado
Endpoint /ingest/pdf ✅ Completado
Tests unitarios de CRUD, services y orchestrador ✅ Completado
Tests de endpoints con FastAPI TestClient ✅ Completado
Colección Postman para todos los endpoints ✅ Completado
CI / CD con GitHub Actions (deploy automático)    🚧 En progreso
Soporte PostgreSQL en producción 🚧 En progreso
Documentación OpenAPI completa 🚧 En revisión
Dashboard de monitoreo (Prometheus / Grafana)    🚧 Pendiente
Endpoint de gestión de vídeos PDF 🚧 Pendiente
🛠️ Tecnologías y Dependencias

    Backend & API:

        FastAPI

        Uvicorn

        Pydantic V2

    Descarga de vídeo:

        yt‑dlp

    Audio & ML:

        OpenAI Whisper

        Transformers (Hugging Face)

        Sentence‑Transformers

        PyTorch

    PDF:

        PyMuPDF (fitz)

        pdfplumber

    BD & Migrations:

        SQLAlchemy ORM

        Alembic

    Testing:

        pytest

        httpx (TestClient)

    Infra & DevOps:

        Docker

        GitHub Actions

        (Próximamente K8s & Helm)

📁 Estructura del Proyecto

DEOS/
├── app/
│ ├── api/
│ │ ├── audio.py # Endpoints de audio
│ │ ├── videos.py # Endpoints de vídeos
│ │ ├── ingestion.py # Endpoints PDF
│ │ └── classify.py # (Pendiente)
│ ├── core/
│ │ ├── config.py # Settings (pydantic-settings)
│ │ └── logger.py # Configuración de logging
│ ├── db/
│ │ ├── session.py # Engine, Base y get_db
│ │ ├── models.py # SQLAlchemy models
│ │ ├── crud.py # Funciones CRUD
│ │ └── alembic/ # Migraciones
│ ├── services/
│ │ ├── downloader.py # descarga con yt-dlp
│ │ ├── transcriber.py # llamada a Whisper
│ │ ├── summarization.py # Hugging Face summaries
│ │ ├── classifier.py # sentence-transformers
│ │ ├── orchestrator.py # pipeline audio & PDF
│ │ └── pdf_processor.py # extracción y persistencia de PDF
│ └── main.py # App, routers e inicio
├── tests/ # pytest tests
│ ├── test_*_api.py # endpoints
│ ├── test_crud.py # CRUD unitarios
│ └── test_orchestrator*.py # flujos completos
├── docs/
│ ├── postman_collection.json
│ └── architecture.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md # ← ¡Tú estás aquí!
└── .github/
└── workflows/
└── ci.yml # Tests + lint + build + deploy

🚀 Guía de Uso

1. Instalación

git clone https://github.com/tu-org/DEOS.git
cd DEOS
python3.9 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

    Requisito: Python ≥ 3.9

2. Configuración

Edita app/core/config.py o crea un .env con:

DATABASE_URL=sqlite:///./data/deos.db
DOWNLOAD_DIR=./data/downloads
LOG_LEVEL=INFO

3. Ejecutar en Local

uvicorn app.main:app --reload

    Docs interactivos

        Swagger: http://127.0.0.1:8000/docs

        ReDoc: http://127.0.0.1:8000/redoc

4. Docker (opcional)

docker-compose up --build

📡 API & Endpoints
/audio/download (POST)

    Body:

{ "url": "https://www.youtube.com/watch?v=..." }

Response:

    {
      "filename": "...mp3",
      "title": "...",
      "duration": 123.4,
      "page_url": "...youtube..."
    }

/videos/list (GET)

    Pendiente: listará los vídeos ya procesados.

/ingest/pdf (POST)

    Form‑data:

        file: archivo PDF

        topic (opcional)

        level (opcional, e.g. “short”/“medium”/“long”)

    Response:

    {
      "file_path": "data/downloads/test.pdf",
      "topic": "miTema",
      "level": "short",
      "extracted_text": "...",
      "summary": "...",
      "tags": [{ "tag": "...", "score": 0.9 }, …]
    }

🧪 Testing

    Unitarios

    pytest tests/test_crud.py tests/test_downloader.py …

    Integración

        Test de endpoints vía fastapi.testclient

        Orquestador completo

    Postman

        Importa docs/postman_collection.json

        Ejecuta la carpeta “DEOS Service” en Postman, revisa variables de entorno

        Verifica todos los métodos (audio, PDF, clasificación…)

🌟 Buenas Prácticas

    Dependencias acotadas en requirements.txt.

    Tests completos: > 90% de coverage en servicios, CRUD y orquestación.

    Linter & Formatter: configuración de black y flake8 en el pipeline CI.

    DI SQLAlchemy: sesiones por dependencia (get_db).

    Logging estructurado: nivel configurable, salida a consola y fichero.

    Migrations: control de esquema con Alembic.

🚧 Despliegue en Producción

    CI/CD con GitHub Actions:

        Run tests → Lint → Build Docker image → Push a registry

        Despliegue automático a staging

        Aprobar despliegue a prod manualmente

    Infraestructura

        Kubernetes (Helm charts) con 2 réplicas, auto‑scale

        PostgreSQL gestionado (AWS RDS / Cloud SQL)

    Monitoreo & Alertas

        Exponer métricas Prometheus

        Dashboards en Grafana

        Alertas Slack/Email para errores 5xx o latencias altas

🤝 Contribuir

    Haz un fork y crea una branch.

    Sigue la Guía de Estilo (.github/CONTRIBUTING.md).

    Añade tests para nuevas funcionalidades.

    Abre Pull Request.

📄 Licencia

Este proyecto está bajo la licencia MIT. Lee el archivo LICENSE para más detalles.

    DEOS: de la extracción profunda al despliegue robusto. ¡Bienvenido/a!