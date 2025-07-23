# 🚀 SOLUCIÓN RÁPIDA - Configurar Python 3.12 para DEOS

## 🎯 Problema identificado:
- Python 3.13 no tiene PyTorch compatible todavía
- Necesitamos usar Python 3.12 específicamente

## ⚡ SOLUCIÓN PASO A PASO (5 minutos):

### 1️⃣ Instalar Python 3.12 vía Homebrew
```bash
# Asegurar que Homebrew funcione
brew update

# Instalar Python 3.12 específicamente
brew install python@3.12

# Verificar instalación
/opt/homebrew/bin/python3.12 --version
```

### 2️⃣ Eliminar entorno virtual actual
```bash
# Desde el directorio DEOS
rm -rf .venv
```

### 3️⃣ Crear nuevo entorno con Python 3.12
```bash
# Usar la ruta completa de Python 3.12
/opt/homebrew/bin/python3.12 -m venv .venv

# Activar el entorno
source .venv/bin/activate

# Verificar que funciona
python --version  # Debe mostrar Python 3.12.x
```

### 4️⃣ Instalar PyTorch primero (compatible)
```bash
# Con el entorno activado, instalar PyTorch para CPU
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Verificar PyTorch
python -c "import torch; print(f'PyTorch {torch.__version__} instalado')"
```

### 5️⃣ Instalar resto de dependencias
```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias sin PyTorch (para evitar conflictos)
pip install fastapi uvicorn[standard] yt-dlp pydantic pydantic-settings
pip install pytest httpx openai-whisper transformers sentence-transformers
pip install SQLAlchemy alembic pdfplumber reportlab PyMuPDF
pip install python-multipart scikit-learn numpy tiktoken
```

### 6️⃣ Verificar instalación
```bash
# Verificar que todo funciona
python -c "import fastapi, torch, whisper; print('✅ Todo instalado correctamente')"

# Probar DEOS
python run_deos.py
```

## 🔧 Si algo falla:

### Problema: No encuentra python3.12
```bash
# Añadir al PATH
export PATH="/opt/homebrew/bin:$PATH"

# O usar ruta completa
/opt/homebrew/bin/python3.12 -m venv .venv
```

### Problema: PyTorch sigue fallando
```bash
# Instalar versión específica compatible
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0
```

### Problema: openai-whisper falla
```bash
# Instalar desde git si la versión de PyPI falla
pip install git+https://github.com/openai/whisper.git
```

## 🎯 Para PyCharm:

1. **Settings** → **Python Interpreter**
2. **Add Interpreter** → **Existing Environment**
3. **Interpreter path**: `/ruta/a/DEOS/.venv/bin/python`
4. **Apply** y **OK**

## ✅ Verificación final:

Si todo funciona, deberías ver:
```bash
(.venv) lolo@MacBook-Pro DEOS % python run_deos.py
🚀 DEOS Service - Iniciando servidor...
==================================================
✅ Python 3.12.x - Compatible
✅ Dependencias principales encontradas
✅ Directorios de datos configurados
✅ Configuración completada
🌐 Iniciando servidor FastAPI...
```

---

## 🚀 ALTERNATIVA AUTOMÁTICA:

Si prefieres un script automático que haga todo esto:
```bash
python3 fix_python_pytorch.py
```