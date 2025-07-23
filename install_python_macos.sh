#!/bin/bash

# 🚀 DEOS - Instalador de Python 3.12 para macOS
# Script que instala Python 3.12 vía Homebrew y configura DEOS

set -e

echo "🚀 DEOS - Instalador de Python 3.12 para macOS"
echo "=============================================="

# Verificar que estamos en el directorio correcto
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio raíz de DEOS"
    exit 1
fi

# Función para verificar si Homebrew está instalado
check_homebrew() {
    if command -v brew >/dev/null 2>&1; then
        echo "✅ Homebrew está instalado"
        return 0
    else
        echo "❌ Homebrew no está instalado"
        return 1
    fi
}

# Función para instalar Homebrew
install_homebrew() {
    echo "📦 Instalando Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Añadir Homebrew al PATH para Apple Silicon Macs
    if [[ $(uname -m) == "arm64" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
        eval "$(/opt/homebrew/bin/brew shellenv)"
    else
        echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zshrc
        eval "$(/usr/local/bin/brew shellenv)"
    fi
    
    echo "✅ Homebrew instalado"
}

# Función para instalar Python 3.12
install_python() {
    echo "🐍 Instalando Python 3.12..."
    
    # Actualizar Homebrew
    brew update
    
    # Instalar Python 3.12
    brew install python@3.12
    
    # Verificar instalación
    if command -v python3.12 >/dev/null 2>&1; then
        PYTHON_VERSION=$(python3.12 --version)
        echo "✅ $PYTHON_VERSION instalado exitosamente"
        return 0
    else
        echo "❌ Error: Python 3.12 no se instaló correctamente"
        return 1
    fi
}

# Función para configurar el PATH
setup_path() {
    echo "🔧 Configurando PATH..."
    
    # Detectar shell y archivo de configuración
    if [[ $SHELL == *"zsh"* ]]; then
        SHELL_CONFIG="$HOME/.zshrc"
    elif [[ $SHELL == *"bash"* ]]; then
        SHELL_CONFIG="$HOME/.bash_profile"
    else
        SHELL_CONFIG="$HOME/.profile"
    fi
    
    # Añadir Homebrew Python al PATH
    if [[ $(uname -m) == "arm64" ]]; then
        # Apple Silicon Mac
        PYTHON_PATH="/opt/homebrew/bin"
        HOMEBREW_PATH="/opt/homebrew/bin"
    else
        # Intel Mac
        PYTHON_PATH="/usr/local/bin"
        HOMEBREW_PATH="/usr/local/bin"
    fi
    
    # Verificar si ya está en el PATH
    if ! grep -q "$PYTHON_PATH" "$SHELL_CONFIG" 2>/dev/null; then
        echo "export PATH=\"$HOMEBREW_PATH:\$PATH\"" >> "$SHELL_CONFIG"
        echo "✅ PATH actualizado en $SHELL_CONFIG"
    else
        echo "✅ PATH ya configurado"
    fi
    
    # Aplicar cambios al PATH actual
    export PATH="$HOMEBREW_PATH:$PATH"
}

# Función para crear entorno virtual
create_venv() {
    echo "🔨 Creando entorno virtual con Python 3.12..."
    
    # Eliminar entorno anterior si existe
    if [ -d ".venv" ]; then
        echo "🗑️  Eliminando entorno virtual anterior..."
        rm -rf .venv
    fi
    
    # Buscar Python 3.12
    PYTHON_CMD=""
    for cmd in python3.12 /opt/homebrew/bin/python3.12 /usr/local/bin/python3.12; do
        if command -v "$cmd" >/dev/null 2>&1; then
            PYTHON_CMD="$cmd"
            break
        fi
    done
    
    if [ -z "$PYTHON_CMD" ]; then
        echo "❌ Error: No se encontró Python 3.12"
        echo "💡 Intenta: brew install python@3.12"
        exit 1
    fi
    
    echo "🎯 Usando: $PYTHON_CMD"
    VERSION=$($PYTHON_CMD --version)
    echo "✅ Versión: $VERSION"
    
    # Crear entorno virtual
    $PYTHON_CMD -m venv .venv
    
    # Activar entorno virtual
    source .venv/bin/activate
    
    # Verificar versión en entorno virtual
    echo "✅ Entorno virtual creado"
    echo "📋 Versión en entorno virtual: $(python --version)"
    
    # Actualizar pip
    echo "📦 Actualizando pip..."
    python -m pip install --upgrade pip
    
    # Instalar dependencias
    echo "📥 Instalando dependencias..."
    pip install -r requirements.txt
    
    echo "✅ Dependencias instaladas"
}

# Función para verificar instalación
verify_installation() {
    echo "🔍 Verificando instalación..."
    
    # Activar entorno virtual
    source .venv/bin/activate
    
    # Verificar versión de Python
    PYTHON_VERSION=$(python --version)
    echo "✅ Python en entorno virtual: $PYTHON_VERSION"
    
    # Verificar dependencias principales
    if python -c "import fastapi, uvicorn; print('✅ FastAPI y Uvicorn disponibles')" 2>/dev/null; then
        echo "✅ Dependencias principales verificadas"
        return 0
    else
        echo "❌ Error: Faltan dependencias principales"
        return 1
    fi
}

# Función principal
main() {
    echo "🔍 Verificando estado del sistema..."
    
    # Verificar/Instalar Homebrew
    if ! check_homebrew; then
        echo "📦 Instalando Homebrew..."
        install_homebrew
    fi
    
    # Configurar PATH
    setup_path
    
    # Verificar si Python 3.12 ya está instalado
    if command -v python3.12 >/dev/null 2>&1; then
        EXISTING_VERSION=$(python3.12 --version)
        echo "✅ $EXISTING_VERSION ya está instalado"
    else
        install_python
    fi
    
    # Crear entorno virtual y instalar dependencias
    create_venv
    
    # Verificar instalación
    if verify_installation; then
        echo ""
        echo "🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!"
        echo "========================================"
        echo "✅ Python 3.12 instalado vía Homebrew"
        echo "✅ Entorno virtual creado y configurado"
        echo "✅ Dependencias instaladas"
        echo ""
        echo "📋 SIGUIENTES PASOS:"
        echo "1. Reinicia tu terminal o ejecuta: source ~/.zshrc"
        echo "2. Activa el entorno: source .venv/bin/activate"
        echo "3. Ejecuta DEOS: python run_deos.py"
        echo ""
        echo "🔧 COMANDOS ÚTILES:"
        echo "   • Activar entorno: source .venv/bin/activate"
        echo "   • Ejecutar servidor: python run_deos.py"
        echo "   • Ver versión Python: python --version"
        echo ""
        echo "💡 Si PyCharm no detecta el nuevo Python:"
        echo "   Settings → Python Interpreter → Add → Existing → .venv/bin/python"
    else
        echo "❌ Error en la verificación final"
        exit 1
    fi
}

# Ejecutar función principal
main