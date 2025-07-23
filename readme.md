# 🎵 DEOS - Deep Extraction, Orchestration & Summarization

DEOS es un microservicio FastAPI que permite descargar, transcribir, resumir y clasificar contenido de YouTube y documentos PDF de manera automática e inteligente.

## 🚀 Inicio Rápido

### Ejecutar DEOS (5 opciones disponibles):

1. **Doble-click (macOS):** `start_deos.command`
2. **Script rápido:** `./start_deos.sh`
3. **Script Python:** `python run_deos.py`
4. **PyCharm:** Usar configuración "DEOS Server"
5. **Directo:** `uvicorn app.main:app --reload`

### Probar la API:
- **Swagger UI:** http://localhost:8000/docs
- **Postman:** Importar `DEOS_Postman_Collection.json`

## 📚 **Documentación Completa**

### 🎯 **Para Desarrolladores Frontend**
- **[📖 API Documentation](docs/FRONTEND_API_DOCUMENTATION.md)** - Guía completa para crear frontends que consuman DEOS
  - Endpoints detallados con ejemplos
  - Guía de UX/UI recomendada
  - Manejo de errores y casos de uso
  - Flujos de trabajo completos

### 🚀 **Para Despliegue en Producción**
- **[🛠️ Deployment Roadmap](docs/DEPLOYMENT_ROADMAP.md)** - Plan paso a paso para llevar DEOS a producción
  - Opciones de hosting (DigitalOcean, AWS, VPS)
  - Containerización con Docker
  - CI/CD con GitHub Actions
  - Monitoreo y seguridad
  - Estimaciones de costos

### 🌟 **Para Expansión del Proyecto**
- **[🚀 Future Enhancements](docs/FUTURE_ENHANCEMENTS.md)** - Roadmap de mejoras y nuevas funcionalidades
  - Features de corto, medio y largo plazo
  - Casos de uso específicos (educación, corporate, media)
  - Integración con nuevas plataformas
  - Ideas innovadoras con IA

### 🧪 **Para Testing**
- **[📬 Postman Guide](POSTMAN_TESTING_GUIDE.md)** - Guía completa de testing con Postman

## 🔧 Funcionalidades Principales

- **🎵 Descarga de audio** desde YouTube
- **📝 Transcripción** con OpenAI Whisper
- **📋 Resumen** automático con multiple niveles
- **🏷️ Clasificación** semántica con scores
- **📄 Ingesta de PDFs** con extracción de texto
- **🔄 Pipeline completo** en un solo endpoint (`/process`)

## 🛠️ Requerimientos

- Python 3.9+
- ffmpeg (para procesamiento de audio)
- 4GB+ RAM recomendado

## 📦 Instalación

```bash
# Clonar repositorio
git clone [repository-url]
cd deos

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python run_deos.py
```

## 🧪 Testing

```bash
# Tests unitarios
python -m pytest tests/ -v

# Postman collection
# Importar DEOS_Postman_Collection.json en Postman
```

## 📊 API Endpoints

- `POST /process` - **⭐ Endpoint principal** - Pipeline completo
- `POST /audio/download` - Descarga audio de YouTube
- `POST /audio/transcribe` - Transcribe audio a texto
- `POST /audio/summarize` - Resume texto
- `POST /classify` - Clasifica contenido
- `GET /videos/` - Lista videos procesados
- `POST /ingest/pdf` - Procesa documentos PDF

**Ver documentación completa en:** http://localhost:8000/docs

## 🎯 Próximos Pasos

### **Inmediato:**
1. **Frontend Development** usando `docs/FRONTEND_API_DOCUMENTATION.md`
2. **Production Deployment** siguiendo `docs/DEPLOYMENT_ROADMAP.md`

### **Corto plazo:**
- Dashboard analytics
- Batch processing
- Sentiment analysis
- Enterprise features

### **Ideas futuras:**
- Mobile apps
- Nuevas plataformas (Twitch, Podcasts)
- IA conversacional
- Multi-idioma

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Ve el roadmap de mejoras futuras para ideas de desarrollo.

## 📄 Licencia

[Especificar licencia]

---

**🚀 DEOS - Transformando contenido multimedia en insights accionables**