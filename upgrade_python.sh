#!/bin/bash

# 🚀 DEOS - Script rápido de actualización de Python
# Actualiza el entorno virtual de Python 3.8 a Python 3.9+

set -e

echo "🚀 DEOS - Actualizando entorno Python"
echo "======================================"

# Verificar que estamos en el directorio correcto
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio raíz del proyecto DEOS"
    exit 1
fi

# Verificar versión de Python del sistema
echo "🔍 Verificando Python del sistema..."
PYTHON_VERSION=$(python3 --version)
echo "✅ Encontrado: $PYTHON_VERSION"

# Salir del entorno virtual si está activo
if [ -n "$VIRTUAL_ENV" ]; then
    echo "🔄 Desactivando entorno virtual actual..."
    deactivate 2>/dev/null || true
fi

# Hacer backup de requirements.txt
if [ -f "requirements.txt" ]; then
    echo "💾 Haciendo backup de requirements.txt..."
    cp requirements.txt requirements.txt.backup
fi

# Eliminar entorno virtual anterior
if [ -d ".venv" ]; then
    echo "🗑️  Eliminando entorno virtual anterior..."
    rm -rf .venv
fi

# Crear nuevo entorno virtual
echo "🔨 Creando nuevo entorno virtual con Python 3.13..."
python3 -m venv .venv

# Activar el nuevo entorno virtual
echo "🔄 Activando nuevo entorno virtual..."
source .venv/bin/activate

# Verificar nueva versión
echo "✅ Nueva versión en entorno virtual:"
python --version

# Actualizar pip
echo "📦 Actualizando pip..."
python -m pip install --upgrade pip

# Instalar dependencias
if [ -f "requirements.txt" ]; then
    echo "📥 Instalando dependencias..."
    pip install -r requirements.txt
    echo "✅ Dependencias instaladas"
else
    echo "⚠️  No se encontró requirements.txt"
fi

# Verificar instalación
echo "🔍 Verificando instalación..."
python -c "import fastapi, uvicorn; print('✅ FastAPI y Uvicorn disponibles')" 2>/dev/null || echo "⚠️  Algunas dependencias pueden faltar"

echo ""
echo "🎉 ¡ACTUALIZACIÓN COMPLETADA!"
echo "=============================="
echo ""
echo "📋 SIGUIENTES PASOS:"
echo "1. El entorno virtual ya está activado"
echo "2. Ejecuta: python run_deos.py"
echo "3. Para futuros usos: source .venv/bin/activate"
echo ""
echo "🔧 COMANDOS ÚTILES:"
echo "   • Ejecutar servidor: python run_deos.py"
echo "   • Ver versión: python --version"
echo "   • Ejecutar tests: python -m pytest tests/ -v"
echo ""