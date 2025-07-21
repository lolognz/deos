# 🚀 Guía Rápida - Proyecto DEOS 

## ⚡ Comandos Rápidos

### En macOS/PyCharm:

```bash
# 1. Script automático (recomendado)
./run_deos.sh status    # Ver estado del sistema
./run_deos.sh setup     # Configurar todo desde cero
./run_deos.sh test      # Ejecutar todos los tests  
./run_deos.sh serve     # Levantar servidor en modo desarrollo
./run_deos.sh serve-bg  # Levantar servidor en background
./run_deos.sh stop      # Parar servidor background
```

### Manual (paso a paso):

```bash
# 1. Activar entorno virtual
source .venv/bin/activate

# 2. Levantar servidor
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 3. Ejecutar tests
python -m pytest tests/ -v

# 4. Verificar base de datos
ls -la data/
```

## 🌐 URLs Importantes

- **API Docs**: http://localhost:8000/docs
- **API Alternative**: http://localhost:8000/redoc  
- **Base URL**: http://localhost:8000

## 🧪 Testing con Postman/curl

### 1. Clasificar Texto
```bash
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{"text": "Video sobre inteligencia artificial", "top_k": 3}'
```

### 2. Obtener Videos
```bash
curl "http://localhost:8000/videos/"
```

### 3. Procesar Video YouTube
```bash
curl -X POST "http://localhost:8000/audio/process" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/watch?v=XXXXXX", "topic": "tecnologia"}'
```

### 4. Resumir Texto
```bash
curl -X POST "http://localhost:8000/audio/summarize" \
     -H "Content-Type: application/json" \
     -d '{"text": "Texto largo a resumir...", "summary_type": "medium"}'
```

### 5. Subir PDF
```bash
curl -X POST "http://localhost:8000/ingestion/pdf" \
     -F "file=@documento.pdf" \
     -F "topic=investigacion"
```

## 📁 Estructura del Proyecto

```
📦 DEOS/
├── 🚀 run_deos.sh          # Script principal
├── 📋 postman_examples.json # Ejemplos para Postman
├── 📖 GUIA_RAPIDA.md        # Esta guía
├── 🏗️ app/                 # Código principal
│   ├── 🌐 api/              # Endpoints FastAPI
│   ├── 🔧 services/         # Lógica de negocio
│   ├── 🗄️ db/              # Base de datos
│   └── ⚙️ core/            # Configuración
├── 🧪 tests/               # Tests unitarios
├── 📊 data/                # Base de datos SQLite
└── 🐍 .venv/               # Entorno virtual
```

## 🔧 Funcionalidades Principales

### ✅ **Funcionando Perfectamente:**
- ✅ Procesamiento de audio de YouTube (descarga + transcripción + resumen + clasificación)
- ✅ Procesamiento de PDFs (extracción + resumen + clasificación)  
- ✅ API REST completa con FastAPI
- ✅ Base de datos SQLite con modelos completos
- ✅ Sistema de clasificación automática por temas
- ✅ Generación de resúmenes en diferentes niveles
- ✅ Tests unitarios e integración (30/30 ✅)

### 🎯 **Endpoints Disponibles:**
- `POST /audio/process` - Procesar video YouTube
- `POST /ingestion/pdf` - Subir y procesar PDF
- `POST /classify` - Clasificar texto por temas
- `POST /audio/summarize` - Resumir texto
- `GET /videos/` - Listar videos procesados
- `GET /videos/{id}` - Detalles de un video

## 🚨 Problemas Comunes

### Puerto ocupado:
```bash
# Ver qué usa el puerto 8000
lsof -i :8000

# Matar proceso en puerto 8000
kill -9 $(lsof -t -i:8000)
```

### Error de dependencias:
```bash
./run_deos.sh setup  # Reinstalar todo
```

### Base de datos corrupta:
```bash
rm data/deos.db
./run_deos.sh setup
```

## 📱 Para PyCharm

1. **Configurar intérprete**: `.venv/bin/python`
2. **Run Configuration**: 
   - Script: `uvicorn`
   - Parameters: `app.main:app --reload`
   - Working directory: `/path/to/deos`
3. **Tests**: Pytest con directorio `tests/`

## 🎉 ¡Listo para Usar!

Tu proyecto DEOS está completamente restaurado y funcional. Todos los tests pasan, la API funciona perfectamente, y tanto el procesamiento de YouTube como PDFs están operativos.

**Siguiente paso recomendado**: Probar con videos reales de YouTube y documentos PDF para verificar el flujo completo.