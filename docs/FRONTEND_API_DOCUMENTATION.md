# 🚀 DEOS API - Documentación para Frontend

## 📖 Descripción General

**DEOS** (Deep Extraction, Orchestration & Summarization) es una API REST que procesa contenido multimedia y documentos para extraer, transcribir, resumir y clasificar información automáticamente.

### 🎯 Funcionalidades Principales
- **Descarga y procesamiento** de videos de YouTube
- **Transcripción automática** usando OpenAI Whisper
- **Resumen inteligente** con múltiples niveles
- **Clasificación semántica** con etiquetas y scores
- **Ingesta de PDFs** con extracción de texto
- **Gestión de contenido** procesado con filtros y búsqueda

---

## 🌐 Información del Servidor

### URLs Base
- **Desarrollo Local:** `http://localhost:8000`
- **Documentación Interactiva:** `http://localhost:8000/docs`
- **Esquema OpenAPI:** `http://localhost:8000/openapi.json`

### Autenticación
- **Tipo:** Actualmente sin autenticación
- **Headers requeridos:** `Content-Type: application/json` (para requests JSON)

---

## 📚 Endpoints de la API

### 🎵 **Audio Processing**

#### `POST /audio/download`
Descarga audio desde YouTube y lo guarda localmente.

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Response (200):**
```json
{
  "path": "data/downloads/audio_12345.mp3",
  "title": "Rick Astley - Never Gonna Give You Up",
  "duration": 213,
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Tiempos esperados:** 10-30 segundos

---

#### `POST /audio/download/bulk`
Descarga múltiples audios en segundo plano.

**Request:**
```json
{
  "urls": [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=2g811Eo7K8U"
  ]
}
```

**Response (200):**
```json
{
  "tasks": [
    {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "status": "queued"},
    {"url": "https://www.youtube.com/watch?v=2g811Eo7K8U", "status": "queued"}
  ]
}
```

---

#### `POST /audio/transcribe`
Transcribe un archivo de audio a texto.

**Request:**
```json
{
  "file_path": "data/downloads/audio_12345.mp3"
}
```

**Response (200):**
```json
{
  "transcription": "Never gonna give you up, never gonna let you down...",
  "duration": 213.5
}
```

**Tiempos esperados:** 5-15 segundos

---

#### `POST /audio/summarize`
Genera un resumen del texto transcrito.

**Request:**
```json
{
  "text": "Never gonna give you up, never gonna let you down...",
  "level": "short"
}
```

**Parámetros de level:**
- `"short"` - Resumen breve (1-2 frases)
- `"medium"` - Resumen moderado (1 párrafo)
- `"detailed"` - Resumen detallado (múltiples párrafos)

**Response (200):**
```json
{
  "summary": "Canción pop de Rick Astley sobre compromiso y lealtad romántica."
}
```

---

### 🔄 **Pipeline Completo**

#### `POST /process`
**⭐ ENDPOINT PRINCIPAL** - Ejecuta todo el pipeline de procesamiento.

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "topic": "music",
  "summary_level": "medium"
}
```

**Response (200):**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "audio_path": "data/downloads/audio_12345.mp3",
  "title": "Rick Astley - Never Gonna Give You Up",
  "duration": 213,
  "transcript": "Never gonna give you up, never gonna let you down...",
  "transcript_duration": 213.5,
  "summary": "Canción pop icónica de Rick Astley sobre compromiso romántico, conocida por el fenómeno 'Rickrolling'.",
  "topic": "music",
  "tags": [
    {"tag": "música", "score": 0.95},
    {"tag": "pop", "score": 0.89},
    {"tag": "entretenimiento", "score": 0.76}
  ]
}
```

**Tiempos esperados:** 15-45 segundos

---

### 🏷️ **Clasificación**

#### `POST /classify`
Clasifica texto en categorías semánticas.

**Request:**
```json
{
  "text": "Esta es una charla sobre inteligencia artificial y machine learning",
  "top_k": 3,
  "threshold": 0.1
}
```

**Response (200):**
```json
{
  "tags": [
    {"tag": "tecnología", "score": 0.92},
    {"tag": "educación", "score": 0.78},
    {"tag": "ciencia", "score": 0.65}
  ]
}
```

---

### 🎬 **Gestión de Videos**

#### `GET /videos/`
Lista videos procesados con filtros opcionales.

**Query Parameters:**
- `skip` (int): Offset para paginación (default: 0)
- `limit` (int): Número máximo de resultados (default: 100)
- `topic` (string): Filtrar por tema
- `tag` (string): Filtrar por etiqueta de clasificación
- `date_from` (datetime): Fecha mínima (ISO format)
- `date_to` (datetime): Fecha máxima (ISO format)

**Ejemplo:** `GET /videos/?skip=0&limit=10&topic=music&tag=pop`

**Response (200):**
```json
[
  {
    "id": 1,
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "title": "Rick Astley - Never Gonna Give You Up",
    "duration": 213,
    "topic": "music",
    "created_at": "2025-07-23T23:01:20.974Z"
  }
]
```

---

#### `GET /videos/{video_id}`
Obtiene detalles completos de un video específico.

**Response (200):**
```json
{
  "id": 1,
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "title": "Rick Astley - Never Gonna Give You Up",
  "duration": 213,
  "topic": "music",
  "created_at": "2025-07-23T23:01:20.974Z",
  "audio": {
    "path": "data/downloads/audio_12345.mp3",
    "created_at": "2025-07-23T23:01:25.123Z"
  },
  "transcript": {
    "text": "Never gonna give you up...",
    "created_at": "2025-07-23T23:01:30.456Z"
  },
  "summary": {
    "level": "medium",
    "text": "Canción pop icónica...",
    "created_at": "2025-07-23T23:01:35.789Z"
  },
  "classifications": [
    {"tag": "música", "score": 0.95, "created_at": "2025-07-23T23:01:40.123Z"},
    {"tag": "pop", "score": 0.89, "created_at": "2025-07-23T23:01:40.123Z"}
  ]
}
```

**Response (404):**
```json
{
  "detail": "Video not found"
}
```

---

### 📄 **Ingesta de PDFs**

#### `POST /ingest/pdf`
Procesa un archivo PDF completamente.

**Request:** `multipart/form-data`
- `file`: Archivo PDF (requerido)
- `topic`: Tema del documento (opcional, default: "default")
- `level`: Nivel de resumen (opcional, default: "short")

**Response (200):**
```json
{
  "message": "PDF procesado correctamente",
  "file_path": "data/downloads/document.pdf",
  "topic": "research",
  "level": "short",
  "extracted_text": "Contenido extraído del PDF...",
  "summary": "Resumen del documento...",
  "tags": [
    {"tag": "investigación", "score": 0.88},
    {"tag": "ciencia", "score": 0.72}
  ]
}
```

---

## 🎨 **Guía de UX/UI para Frontend**

### 🎯 **Páginas/Vistas Sugeridas**

#### 1. **Dashboard Principal**
- **Estadísticas:** Total de videos/PDFs procesados, tiempo total, categorías más populares
- **Actividad reciente:** Últimos contenidos procesados
- **Acceso rápido:** Botones para "Procesar Video" y "Subir PDF"

#### 2. **Procesador de Videos** (`/process`)
- **Input:** Campo URL de YouTube con validación
- **Opciones:** Selector de tema y nivel de resumen
- **Progreso:** Barra de progreso en tiempo real
- **Resultados:** Vista previa del contenido procesado

#### 3. **Explorador de Contenido** (`/videos/`)
- **Filtros:** Por tema, fecha, etiquetas
- **Vista de lista/grid:** Con miniaturas y metadatos básicos
- **Búsqueda:** Por título, contenido o etiquetas
- **Paginación:** Para grandes volúmenes de contenido

#### 4. **Vista Detalle** (`/videos/{id}`)
- **Información completa:** Transcripción, resumen, clasificaciones
- **Audio player:** Para reproducir el audio extraído
- **Timeline:** Navegación por la transcripción
- **Acciones:** Descargar, compartir, re-procesar

#### 5. **Clasificador Individual** (`/classify`)
- **Input de texto:** Área para texto libre
- **Configuración:** top_k y threshold ajustables
- **Resultados visuales:** Tags con barras de confianza

#### 6. **Subida de PDFs** (`/ingest/pdf`)
- **Drag & drop:** Interfaz intuitiva para subir archivos
- **Preview:** Vista previa del PDF antes de procesar
- **Configuración:** Tema y nivel de resumen

### 🎨 **Elementos de UI Clave**

#### **Estados de Carga**
```javascript
// Estados para el endpoint /process
IDLE -> DOWNLOADING -> TRANSCRIBING -> SUMMARIZING -> CLASSIFYING -> COMPLETED
```

#### **Componentes Reutilizables**
- **VideoCard:** Tarjeta con título, duración, tema, preview
- **TagCloud:** Visualización de clasificaciones con scores
- **ProgressIndicator:** Barra de progreso para pipelines largos
- **FilterPanel:** Panel lateral con filtros múltiples
- **ResultsDisplay:** Vista unificada para mostrar resultados

#### **Notificaciones**
- **Success:** Procesamiento completado
- **Error:** URLs inválidas, archivos corruptos
- **Warning:** Procesos que toman más tiempo del esperado
- **Info:** Estado de colas de procesamiento

### 📱 **Responsividad**
- **Mobile:** Priorizar procesamiento individual
- **Tablet:** Vista híbrida lista/detalle
- **Desktop:** Dashboard completo con múltiples paneles

---

## ⚠️ **Manejo de Errores**

### **Códigos de Estado HTTP**
- **200:** Éxito
- **400:** Request inválido (URL malformada, archivo corrupto)
- **404:** Recurso no encontrado
- **422:** Error de validación (Pydantic)
- **500:** Error interno del servidor

### **Estructura de Errores**
```json
{
  "detail": "Descripción del error"
}
```

### **Errores Comunes**
- **URL de YouTube inválida:** Validar formato antes de enviar
- **Archivo no encontrado:** Verificar que el path existe
- **Timeout:** Procesos largos pueden fallar, implementar retry
- **Límites de contenido:** Videos muy largos pueden causar problemas

---

## 🔧 **Consideraciones Técnicas**

### **Performance**
- **Timeout recomendado:** 60 segundos para `/process`
- **Polling:** Para verificar estado de procesamiento bulk
- **Caché:** Considerar caché del lado cliente para listas

### **Optimizaciones**
- **Lazy loading:** Para listas largas de videos
- **Debounced search:** Para filtros en tiempo real
- **Progressive enhancement:** Cargar detalles bajo demanda

### **Monitoreo**
- **Health check:** `GET /docs` para verificar disponibilidad
- **Metrics:** Tiempo de respuesta por endpoint
- **User feedback:** Reportar errores y mejoras

---

## 🎉 **Funcionalidades Avanzadas Sugeridas**

### **Para el Frontend**
1. **Dashboard Analytics:** Gráficos de uso y tendencias
2. **Batch Processing:** Procesar múltiples URLs simultáneamente
3. **Export/Import:** Exportar datos a JSON/CSV
4. **Favorites:** Sistema de favoritos para contenido
5. **Search:** Búsqueda full-text en transcripciones
6. **Themes:** Modo oscuro/claro
7. **Notifications:** Sistema de notificaciones en tiempo real
8. **Collaboration:** Compartir contenido procesado

### **Integraciones**
- **YouTube API:** Para obtener metadatos adicionales
- **Social Media:** Compartir resultados
- **Cloud Storage:** Backup automático
- **Analytics:** Google Analytics o similar

---

## 📝 **Ejemplo de Flujo Completo**

```javascript
// 1. Usuario ingresa URL
const url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";

// 2. Validar URL
if (!isValidYouTubeURL(url)) {
  showError("URL de YouTube inválida");
  return;
}

// 3. Mostrar loader
showProcessingLoader();

// 4. Procesar
try {
  const response = await fetch('/process', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      url: url,
      topic: "music",
      summary_level: "medium"
    })
  });
  
  const result = await response.json();
  
  // 5. Mostrar resultados
  displayResults(result);
  
} catch (error) {
  showError("Error procesando video: " + error.message);
} finally {
  hideProcessingLoader();
}
```

---

**🔗 Esta documentación está lista para ser utilizada por cualquier desarrollador frontend para crear una interfaz completa que consuma la API DEOS.**