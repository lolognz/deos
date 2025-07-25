#!/usr/bin/env python3
"""
🚀 DEOS Service Runner
Script para ejecutar el servicio DEOS con validaciones y configuración automática.
"""

import sys
import os
import subprocess
from pathlib import Path


def check_python_version():
    """Verifica que la versión de Python sea >= 3.9"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Error: Se requiere Python 3.9 o superior. Versión actual: {version.major}.{version.minor}")
        print("Por favor actualiza Python antes de continuar.")
        sys.exit(1)
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")


def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    try:
        import fastapi
        import uvicorn
        print("✅ Dependencias principales encontradas")
        return True
    except ImportError as e:
        print(f"❌ Error: Dependencia faltante - {e}")
        print("Instala las dependencias con: pip install -r requirements.txt")
        return False


def setup_environment():
    """Configura el entorno si es necesario"""
    # Crear directorios necesarios
    data_dir = Path("data")
    downloads_dir = data_dir / "downloads"
    
    data_dir.mkdir(exist_ok=True)
    downloads_dir.mkdir(exist_ok=True)
    
    print("✅ Directorios de datos configurados")


def main():
    """Función principal"""
    print("🚀 DEOS Service - Iniciando servidor...")
    print("=" * 50)
    
    # Validaciones
    check_python_version()
    
    if not check_dependencies():
        sys.exit(1)
    
    setup_environment()
    
    # Configurar variables de entorno por defecto
    os.environ.setdefault("DOWNLOAD_DIR", "data/downloads")
    os.environ.setdefault("ENV_NAME", "development")
    
    print("✅ Configuración completada")
    print("🌐 Iniciando servidor FastAPI...")
    print("📖 Documentación disponible en: http://localhost:8000/docs")
    print("=" * 50)
    
    # Ejecutar uvicorn
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()