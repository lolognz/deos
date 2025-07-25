# 🧪 Guía de Testing con Postman - DEOS Service

## 📋 Importar la Colección

1. **Abrir Postman**
2. **Importar colección**: `File` → `Import` → Seleccionar `DEOS_Postman_Collection.json`
3. **Crear environment** (opcional pero recomendado):
   - Name: `DEOS Local`
   - Variables:
     - `base_url`: `http://localhost:8000`
     - `test_youtube_url`: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

## 🚀 Ejecutar Tests

### Orden Recomendado de Ejecución

1. **🏥 Health & Status**
   - `API Documentation` - Verificar que la API esté funcionando
   - `OpenAPI Schema` - Validar el esquema de la API

2. **🎵 Audio Endpoints**
   - `Download Audio from YouTube` - ⚠️ **EJECUTAR PRIMERO** (guarda variables para otros tests)
   - `Transcribe Audio` - Usa el archivo del paso anterior
   - `Summarize Text` - Usa la transcripción del paso anterior
   - `Download Bulk Audio` - Test de descarga masiva

3. **🔄 Process Endpoint**
   - `Complete Process Pipeline` - Pipeline completo de extremo a extremo

4. **🏷️ Classification Endpoint**
   - `Classify Text` - Clasificación básica
   - `Classify with Custom Parameters` - Con parámetros personalizados

5. **🎬 Videos Endpoints**
   - `List All Videos` - ⚠️ **EJECUTAR PRIMERO** (guarda ID para otros tests)
   - `List Videos with Pagination` - Con paginación
   - `List Videos with Topic Filter` - Filtrado por tema
   - `List Videos with Date Range` - Filtrado por fechas
   - `Get Video by ID` - Usa ID del primer test
   - `Get Non-existent Video (404 Test)` - Test de error 404

6. **📄 PDF Ingestion**
   - `Ingest PDF (Form Data)` - ⚠️ **Requiere subir un archivo PDF**

7. **❌ Error Cases**
   - `Invalid YouTube URL` - Test de URL inválida
   - `Transcribe Non-existent File` - Test de archivo inexistente
   - `Empty Classification Text` - Test de texto vacío

## 🔄 Ejecución Automática

### Runner de Colección Completa
1. Click derecho en la colección "DEOS Service"
2. Seleccionar "Run collection"
3. Configurar:
   - **Iterations**: 1
   - **Delay**: 2000ms (recomendado para dar tiempo a los procesos)
   - **Data file**: Ninguno (opcional)

### Runner de Carpetas Específicas
Puedes ejecutar solo carpetas específicas:
- Solo tests de Audio: Ejecutar carpeta "🎵 Audio Endpoints"
- Solo tests de Videos: Ejecutar carpeta "🎬 Videos Endpoints"
- Solo tests de errores: Ejecutar carpeta "❌ Error Cases"

## ⚡ Variables de Entorno Automáticas

Los tests están configurados para **guardar automáticamente** variables entre requests:

- `audio_path` - Path del archivo de audio descargado
- `transcription_text` - Texto transcrito del audio
- `video_id` - ID del primer video encontrado

## 📊 Interpretación de Resultados

### Tests Exitosos ✅
- **Status 200**: Operación exitosa
- **Response time < 30s**: Rendimiento aceptable
- **Required fields present**: Estructura de respuesta correcta

### Tests con Advertencias ⚠️
- **404 en Get Video by ID**: Normal si no hay videos en la BD
- **Empty arrays en List Videos**: Normal si la BD está vacía

### Tests que Fallan ❌
- **500 Server Error**: Problema en el servidor
- **422 Validation Error**: Datos de entrada incorrectos
- **Timeout**: El servidor no responde o proceso muy lento

## 🛠️ Solución de Problemas

### Error: Connection refused
```
Solución: Verificar que el servidor DEOS esté ejecutándose en http://localhost:8000
Comando: python run_deos.py
```

### Error: Invalid YouTube URL
```
Solución: Cambiar la variable test_youtube_url por una URL válida de YouTube
```

### Error: PDF Upload fails
```
Solución: 
1. En el request "Ingest PDF", click en "Body" → "form-data"
2. En el campo "file", seleccionar "File" y subir un PDF real
```

### Tiempos de respuesta largos
```
Solución: 
- Los procesos de transcripción y descarga pueden tomar 15-30 segundos
- Aumentar el timeout en Postman: Settings → General → Request timeout
```

## 📈 Métricas Esperadas

| Endpoint | Tiempo Esperado | Notas |
|----------|----------------|-------|
| `/docs` | < 1s | Documentación |
| `/audio/download` | 10-30s | Depende del video |
| `/audio/transcribe` | 5-15s | Depende del audio |
| `/classify` | < 2s | Clasificación rápida |
| `/videos/` | < 1s | Consulta BD |
| `/process` | 15-45s | Pipeline completo |

## 🎯 Coverage de Testing

La colección cubre:
- ✅ **Happy paths**: Flujos normales exitosos
- ✅ **Error handling**: Casos de error esperados
- ✅ **Edge cases**: Casos límite (URLs inválidas, archivos inexistentes)
- ✅ **Integration**: Pipeline completo de extremo a extremo
- ✅ **Data validation**: Validación de estructura de respuestas

---

**💡 Tip**: Ejecuta los tests en orden para maximizar la cobertura, ya que algunos tests dependen de datos creados por tests anteriores.