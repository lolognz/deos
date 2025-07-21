#!/bin/bash

# 🚀 DEOS - Script de Instalación para macOS/PyCharm
# Ejecutar con: bash setup_deos.sh

set -e

# Colores para logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

log() { echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"; }
log_success() { echo -e "${GREEN}[$(date +'%H:%M:%S')] ✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}[$(date +'%H:%M:%S')] ⚠️ $1${NC}"; }
log_error() { echo -e "${RED}[$(date +'%H:%M:%S')] ❌ $1${NC}"; }
log_step() { echo -e "${PURPLE}[$(date +'%H:%M:%S')] 🔧 $1${NC}"; }

echo "=================================================================="
echo -e "${BLUE}🚀 DEOS - Setup Completo para macOS/PyCharm${NC}"
echo "=================================================================="

# Verificar directorio del proyecto
if [ ! -f "app/main.py" ]; then
    log_error "No se encontró app/main.py. ¿Estás en el directorio correcto?"
    exit 1
fi
log_success "Directorio del proyecto verificado"

# Detectar sistema
log_step "Detectando información del sistema..."
PYTHON_VERSION=$(python3 --version 2>/dev/null || echo "No encontrado")
ARCHITECTURE=$(uname -m)
OS_VERSION=$(sw_vers -productVersion 2>/dev/null || echo "Desconocido")

log "Python: $PYTHON_VERSION"
log "Arquitectura: $ARCHITECTURE"
log "macOS: $OS_VERSION"

# Verificar Python 3.8+
PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)' 2>/dev/null || echo 0)
PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)' 2>/dev/null || echo 0)

if [ "$PYTHON_MAJOR" -ne 3 ] || [ "$PYTHON_MINOR" -lt 8 ]; then
    log_error "Se requiere Python 3.8+. Detectado: $PYTHON_VERSION"
    log "Instala con: brew install python@3.12"
    exit 1
fi
log_success "Versión de Python compatible: $PYTHON_VERSION"

# Actualizar requirements.txt
log_step "Actualizando requirements.txt..."
cat > requirements.txt << 'EOF'
fastapi>=0.100.0
uvicorn[standard]>=0.20.0
yt-dlp>=2024.10.22
pydantic>=2.0.0
pydantic-settings>=2.0.0
pytest>=7.0.0
httpx>=0.24.0
openai-whisper
transformers>=4.30.0
sentence-transformers>=2.2.0
torch
torchvision
torchaudio
SQLAlchemy>=2.0.0
alembic>=1.10.0
pdfplumber>=0.9.0
reportlab>=4.0.0
PyMuPDF>=1.20.0
python-multipart>=0.0.5
scikit-learn>=1.0.0
numpy
tiktoken
EOF
log_success "requirements.txt actualizado"

# Backup entorno virtual existente
if [ -d ".venv" ]; then
    log_step "Haciendo backup del entorno virtual..."
    mv .venv .venv_backup_$(date +%Y%m%d_%H%M%S)
    log_success "Backup creado"
fi

# Crear nuevo entorno virtual
log_step "Creando nuevo entorno virtual..."
python3 -m venv .venv
source .venv/bin/activate

if [ "$VIRTUAL_ENV" != "" ]; then
    log_success "Entorno virtual activado: $VIRTUAL_ENV"
else
    log_error "No se pudo activar el entorno virtual"
    exit 1
fi

# Actualizar pip
log_step "Actualizando pip..."
python -m pip install --upgrade pip
log_success "pip actualizado"

# Instalar PyTorch según arquitectura
if [ "$ARCHITECTURE" = "arm64" ]; then
    log_step "Mac M1/M2 detectado - Instalando PyTorch optimizado..."
    python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    if [ $? -ne 0 ]; then
        log_warning "Instalación específica M1/M2 falló, probando estándar..."
        python -m pip install torch torchvision torchaudio
    fi
else
    log_step "Mac Intel detectado - Instalando PyTorch..."
    python -m pip install torch torchvision torchaudio
fi

# Verificar PyTorch
python -c "import torch; print(f'PyTorch {torch.__version__} OK')" 2>/dev/null
if [ $? -eq 0 ]; then
    log_success "PyTorch verificado"
else
    log_error "Error verificando PyTorch"
    exit 1
fi

# Instalar dependencias críticas
log_step "Instalando dependencias básicas..."
python -m pip install wheel setuptools

log_step "Instalando FastAPI..."
python -m pip install "fastapi>=0.100.0" "uvicorn[standard]>=0.20.0"

log_step "Instalando Pydantic..."
python -m pip install "pydantic>=2.0.0" "pydantic-settings>=2.0.0"

log_step "Instalando testing..."
python -m pip install "pytest>=7.0.0" "httpx>=0.24.0"

log_step "Instalando base de datos..."
python -m pip install "SQLAlchemy>=2.0.0" "alembic>=1.10.0"

log_step "Instalando PDFs..."
python -m pip install "pdfplumber>=0.9.0" "reportlab>=4.0.0" "PyMuPDF>=1.20.0"

log_step "Instalando ML..."
python -m pip install "transformers>=4.30.0" "sentence-transformers>=2.2.0" "scikit-learn>=1.0.0"

log_step "Instalando utilidades..."
python -m pip install "yt-dlp>=2024.10.22" "python-multipart>=0.0.5" numpy tiktoken

log_step "Instalando Whisper..."
python -m pip install openai-whisper
if [ $? -eq 0 ]; then
    log_success "Whisper instalado"
else
    log_warning "Error instalando Whisper - continuando"
fi

# Verificar instalaciones críticas
log_step "Verificando instalaciones..."
python -c "import fastapi; print(f'FastAPI {fastapi.__version__}')" && log_success "FastAPI OK"
python -c "import pydantic; print(f'Pydantic {pydantic.__version__}')" && log_success "Pydantic OK"
python -c "import sqlalchemy; print(f'SQLAlchemy {sqlalchemy.__version__}')" && log_success "SQLAlchemy OK"

# Crear estructura de directorios
log_step "Creando directorios..."
mkdir -p data data/downloads
log_success "Directorios creados"

# Inicializar base de datos
log_step "Inicializando base de datos..."
python -c "
import sys
sys.path.append('.')
try:
    from app.db.session import engine, Base
    from app.db.models import Video, Audio, Transcript, Document, Summary, Classification
    Base.metadata.create_all(bind=engine)
    print('Base de datos inicializada')
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
" 2>&1

if [ $? -eq 0 ]; then
    log_success "Base de datos inicializada"
else
    log_error "Error inicializando base de datos"
    exit 1
fi

if [ -f "data/deos.db" ]; then
    log_success "Archivo BD creado: data/deos.db"
fi

# Ejecutar tests
log_step "Ejecutando tests..."
python -m pytest tests/ -v --tb=short -x 2>&1 | head -30
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    log_success "Tests OK"
else
    log_warning "Algunos tests fallaron"
fi

# Probar aplicación
log_step "Probando aplicación..."
timeout 10 python -c "
from app.main import app
from fastapi.testclient import TestClient
client = TestClient(app)
response = client.get('/docs')
print(f'Status /docs: {response.status_code}')
if response.status_code == 200:
    print('✅ Aplicación OK')
else:
    print('❌ Error aplicación')
" 2>&1

echo "=================================================================="
log_success "¡INSTALACIÓN COMPLETADA!"
echo "=================================================================="

echo "📍 Activar entorno:     source .venv/bin/activate"
echo "🚀 Ejecutar servidor:   uvicorn app.main:app --reload"
echo "🧪 Ejecutar tests:      python -m pytest tests/ -v"
echo "📖 Documentación:       http://localhost:8000/docs"
echo ""
echo "✅ .venv/ - Entorno virtual"
echo "✅ data/deos.db - Base de datos"
echo "✅ requirements.txt - Dependencias"

echo "=================================================================="
log_success "¡DEOS listo para usar!"
echo "=================================================================="