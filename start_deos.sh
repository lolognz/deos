#!/bin/bash

# 🚀 DEOS - Iniciador Rápido
# Script para iniciar DEOS desde terminal

set -e

# Cambiar al directorio del script
cd "$(dirname "$0")"

echo "🚀 DEOS - Iniciando servidor..."

# Activar entorno virtual si existe
if [ -d ".venv" ]; then
    echo "🔄 Activando entorno virtual..."
    source .venv/bin/activate
    echo "✅ Entorno virtual activado: $(python --version)"
else
    echo "⚠️  No se encontró entorno virtual .venv"
    echo "   Usando Python del sistema: $(python3 --version)"
fi

# Iniciar DEOS
echo "🌐 Iniciando en: http://localhost:8000"
echo "📖 Documentación: http://localhost:8000/docs"
echo ""

# Ejecutar con el script optimizado
exec python run_deos.py