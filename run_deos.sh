#!/bin/bash

# 🚀 Script para ejecutar el proyecto DEOS en macOS
# Asegúrate de ejecutar: chmod +x run_deos.sh

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m' 
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 DEOS - Sistema de Procesamiento de Contenido${NC}"
echo "================================================"

# Función para mostrar ayuda
show_help() {
    echo -e "${YELLOW}Uso: $0 [comando]${NC}"
    echo ""
    echo "Comandos disponibles:"
    echo "  setup     - Configurar entorno virtual e instalar dependencias"
    echo "  test      - Ejecutar todos los tests"
    echo "  serve     - Levantar servidor de desarrollo" 
    echo "  serve-bg  - Levantar servidor en background"
    echo "  stop      - Parar servidor en background"
    echo "  clean     - Limpiar archivos temporales"
    echo "  status    - Verificar estado del sistema"
    echo "  help      - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  ./run_deos.sh setup"
    echo "  ./run_deos.sh serve"
    echo "  ./run_deos.sh test"
}

# Función para configurar el entorno
setup_env() {
    echo -e "${YELLOW}📦 Configurando entorno virtual...${NC}"
    
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        echo -e "${GREEN}✅ Entorno virtual creado${NC}"
    else
        echo -e "${GREEN}✅ Entorno virtual ya existe${NC}"
    fi
    
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo -e "${YELLOW}🗄️ Configurando base de datos...${NC}"
    if [ ! -d "data" ]; then
        mkdir -p data
    fi
    
    python3 -c "
from app.db.session import engine, Base
from app.db.models import Video, Audio, Transcript, Document, Summary, Classification
Base.metadata.create_all(bind=engine)
print('Base de datos creada exitosamente')
"
    
    echo -e "${GREEN}✅ Configuración completada${NC}"
}

# Función para ejecutar tests
run_tests() {
    echo -e "${YELLOW}🧪 Ejecutando tests...${NC}"
    source .venv/bin/activate
    python -m pytest tests/ -v
    echo -e "${GREEN}✅ Tests completados${NC}"
}

# Función para levantar servidor
serve() {
    echo -e "${YELLOW}🌐 Levantando servidor en http://localhost:8000${NC}"
    echo -e "${BLUE}📖 Documentación: http://localhost:8000/docs${NC}"
    echo -e "${BLUE}Press Ctrl+C to stop${NC}"
    source .venv/bin/activate
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

# Función para levantar servidor en background
serve_bg() {
    echo -e "${YELLOW}🌐 Levantando servidor en background...${NC}"
    source .venv/bin/activate
    nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > server.log 2>&1 &
    echo $! > server.pid
    echo -e "${GREEN}✅ Servidor ejecutándose en background (PID: $(cat server.pid))${NC}"
    echo -e "${BLUE}📖 Documentación: http://localhost:8000/docs${NC}"
    echo -e "${BLUE}📋 Logs: tail -f server.log${NC}"
}

# Función para parar servidor en background
stop_server() {
    if [ -f "server.pid" ]; then
        PID=$(cat server.pid)
        if kill -0 $PID 2>/dev/null; then
            kill $PID
            rm server.pid
            echo -e "${GREEN}✅ Servidor detenido${NC}"
        else
            echo -e "${RED}❌ Servidor ya no está ejecutándose${NC}"
            rm server.pid
        fi
    else
        echo -e "${RED}❌ No se encontró servidor en background${NC}"
    fi
}

# Función para limpiar archivos temporales
clean() {
    echo -e "${YELLOW}🧹 Limpiando archivos temporales...${NC}"
    rm -f server.log server.pid
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -delete
    echo -e "${GREEN}✅ Limpieza completada${NC}"
}

# Función para verificar estado
check_status() {
    echo -e "${YELLOW}📋 Verificando estado del sistema...${NC}"
    
    # Verificar entorno virtual
    if [ -d ".venv" ]; then
        echo -e "${GREEN}✅ Entorno virtual: OK${NC}"
    else
        echo -e "${RED}❌ Entorno virtual: NO ENCONTRADO${NC}"
    fi
    
    # Verificar base de datos
    if [ -f "data/deos.db" ]; then
        echo -e "${GREEN}✅ Base de datos: OK${NC}"
    else
        echo -e "${RED}❌ Base de datos: NO ENCONTRADA${NC}"
    fi
    
    # Verificar servidor
    if [ -f "server.pid" ]; then
        PID=$(cat server.pid)
        if kill -0 $PID 2>/dev/null; then
            echo -e "${GREEN}✅ Servidor: EJECUTÁNDOSE (PID: $PID)${NC}"
        else
            echo -e "${RED}❌ Servidor: DETENIDO${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ Servidor: NO EN BACKGROUND${NC}"
    fi
    
    # Verificar puerto 8000
    if lsof -i :8000 >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Puerto 8000: EN USO${NC}"
    else
        echo -e "${YELLOW}⚠️ Puerto 8000: LIBRE${NC}"
    fi
}

# Main script
case "${1:-help}" in
    setup)
        setup_env
        ;;
    test)
        run_tests
        ;;
    serve)
        serve
        ;;
    serve-bg)
        serve_bg
        ;;
    stop)
        stop_server
        ;;
    clean)
        clean
        ;;
    status)
        check_status
        ;;
    help|*)
        show_help
        ;;
esac