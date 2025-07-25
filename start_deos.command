#!/bin/bash

# 🚀 DEOS - Iniciador Automático para macOS
# Hacer doble-click en este archivo para iniciar DEOS

# Obtener el directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 DEOS - Iniciando automáticamente..."
echo "📂 Directorio: $SCRIPT_DIR"

# Verificar que estamos en el directorio correcto
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: No se encontró app/main.py"
    echo "   Asegúrate de que este archivo esté en el directorio raíz de DEOS"
    read -p "Presiona Enter para cerrar..."
    exit 1
fi

# Verificar que existe el entorno virtual
if [ ! -d ".venv" ]; then
    echo "❌ Error: No se encontró el entorno virtual .venv"
    echo "   Ejecuta primero: python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    read -p "Presiona Enter para cerrar..."
    exit 1
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source .venv/bin/activate

# Verificar Python
PYTHON_VERSION=$(python --version)
echo "✅ $PYTHON_VERSION"

# Verificar dependencias principales
echo "🔍 Verificando dependencias..."
if python -c "import fastapi, uvicorn, torch" 2>/dev/null; then
    echo "✅ Dependencias verificadas"
else
    echo "❌ Error: Faltan dependencias principales"
    echo "   Ejecuta: pip install -r requirements.txt"
    read -p "Presiona Enter para cerrar..."
    exit 1
fi

# Mostrar información
echo ""
echo "🌐 DEOS se iniciará en: http://localhost:8000"
echo "📖 Documentación: http://localhost:8000/docs"
echo "🛑 Para detener: Presiona Ctrl+C"
echo ""

# Iniciar DEOS
echo "🚀 Iniciando servidor DEOS..."
python run_deos.py

# Esperar al usuario antes de cerrar
echo ""
echo "🛑 Servidor detenido."
read -p "Presiona Enter para cerrar esta ventana..."