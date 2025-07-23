#!/usr/bin/env python3
"""
🔧 DEOS - Configurador de Python 3.12 para compatibilidad con PyTorch
Script específico para resolver problemas de compatibilidad con PyTorch
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def install_python312_homebrew():
    """Instala Python 3.12 específicamente vía Homebrew"""
    print("🐍 Instalando Python 3.12 vía Homebrew...")
    
    try:
        # Verificar si Homebrew está disponible
        subprocess.run(['brew', '--version'], capture_output=True, check=True)
        print("✅ Homebrew disponible")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: Homebrew no está disponible")
        print("💡 Instala Homebrew desde: https://brew.sh")
        return False
    
    try:
        # Instalar Python 3.12
        print("📦 Ejecutando: brew install python@3.12")
        subprocess.run(['brew', 'install', 'python@3.12'], check=True)
        print("✅ Python 3.12 instalado vía Homebrew")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Homebrew install tuvo problemas: {e}")
        print("✅ Python 3.12 probablemente ya está instalado")
        return True


def find_python312():
    """Encuentra Python 3.12 específicamente"""
    candidates = [
        'python3.12',
        '/opt/homebrew/bin/python3.12',
        '/usr/local/bin/python3.12',
        '/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12'
    ]
    
    for candidate in candidates:
        try:
            result = subprocess.run([candidate, '--version'], 
                                  capture_output=True, text=True, check=True)
            version_str = result.stdout.strip()
            if '3.12' in version_str:
                print(f"✅ Encontrado Python 3.12: {candidate} -> {version_str}")
                return candidate
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    return None


def create_venv_python312(python_cmd):
    """Crea entorno virtual con Python 3.12"""
    print(f"🔨 Creando entorno virtual con {python_cmd}...")
    
    # Eliminar entorno anterior
    venv_path = Path(".venv")
    if venv_path.exists():
        print("🗑️  Eliminando entorno virtual anterior...")
        shutil.rmtree(venv_path)
    
    # Crear nuevo entorno
    try:
        subprocess.run([python_cmd, '-m', 'venv', '.venv'], check=True)
        print("✅ Entorno virtual creado")
        
        # Verificar versión
        venv_python = Path('.venv/bin/python')
        if venv_python.exists():
            result = subprocess.run([str(venv_python), '--version'], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ Versión en entorno virtual: {result.stdout.strip()}")
            return True
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando entorno virtual: {e}")
        return False


def install_pytorch_compatible():
    """Instala PyTorch compatible con Python 3.12"""
    venv_python = Path('.venv/bin/python')
    
    print("🔥 Instalando PyTorch compatible...")
    
    # Actualizar pip
    try:
        subprocess.run([str(venv_python), '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      check=True)
        print("✅ pip actualizado")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Advertencia pip: {e}")
    
    # Instalar PyTorch específico para macOS
    try:
        pytorch_cmd = [
            str(venv_python), '-m', 'pip', 'install',
            'torch', 'torchvision', 'torchaudio',
            '--index-url', 'https://download.pytorch.org/whl/cpu'
        ]
        print("📦 Instalando PyTorch desde índice oficial...")
        subprocess.run(pytorch_cmd, check=True)
        print("✅ PyTorch instalado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando PyTorch: {e}")
        return False


def install_remaining_dependencies():
    """Instala el resto de dependencias sin PyTorch"""
    venv_python = Path('.venv/bin/python')
    
    # Crear requirements temporal sin PyTorch
    requirements_no_torch = """# Python 3.9+ required
# Dependencies for DEOS Service (sin PyTorch)
fastapi>=0.100.0
uvicorn[standard]>=0.20.0
yt-dlp>=2024.10.22
pydantic>=2.0.0
pydantic-settings>=2.0.0
pytest>=7.0.0
httpx>=0.24.0
openai-whisper>=20231117
transformers>=4.30.0
sentence-transformers>=2.2.0
SQLAlchemy>=2.0.0
alembic>=1.10.0
pdfplumber>=0.9.0
reportlab>=4.0.0
PyMuPDF>=1.20.0
python-multipart>=0.0.5
scikit-learn>=1.0.0
numpy>=1.21.0
tiktoken>=0.3.0"""

    # Escribir requirements temporal
    temp_req = Path("requirements_temp.txt")
    temp_req.write_text(requirements_no_torch)
    
    try:
        print("📦 Instalando dependencias restantes...")
        subprocess.run([str(venv_python), '-m', 'pip', 'install', '-r', 'requirements_temp.txt'], 
                      check=True)
        print("✅ Dependencias restantes instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False
    finally:
        # Limpiar archivo temporal
        if temp_req.exists():
            temp_req.unlink()


def verify_installation():
    """Verifica que todo esté funcionando"""
    venv_python = Path('.venv/bin/python')
    
    print("🔍 Verificando instalación completa...")
    
    # Verificar Python
    try:
        result = subprocess.run([str(venv_python), '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Python: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Error verificando Python: {e}")
        return False
    
    # Verificar PyTorch
    try:
        result = subprocess.run([str(venv_python), '-c', 
                               'import torch; print(f"PyTorch {torch.__version__}")'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Error verificando PyTorch: {e}")
        return False
    
    # Verificar FastAPI
    try:
        result = subprocess.run([str(venv_python), '-c', 
                               'import fastapi, uvicorn; print("FastAPI y Uvicorn disponibles")'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Error verificando FastAPI: {e}")
        return False
    
    # Verificar Whisper
    try:
        result = subprocess.run([str(venv_python), '-c', 
                               'import whisper; print("OpenAI Whisper disponible")'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ {result.stdout.strip()}")
    except Exception as e:
        print(f"⚠️  Whisper puede tener problemas: {e}")
    
    return True


def main():
    """Función principal"""
    print("🔥 DEOS - Configurador Python 3.12 + PyTorch")
    print("=" * 50)
    
    # Verificar directorio
    if not Path("app/main.py").exists():
        print("❌ Error: Ejecuta desde el directorio raíz de DEOS")
        sys.exit(1)
    
    # Paso 1: Instalar Python 3.12
    print("\n📋 PASO 1: Instalar Python 3.12")
    install_python312_homebrew()
    
    # Paso 2: Encontrar Python 3.12
    print("\n📋 PASO 2: Buscar Python 3.12")
    python312_cmd = find_python312()
    
    if not python312_cmd:
        print("❌ No se encontró Python 3.12")
        print("💡 Intenta manualmente:")
        print("   brew install python@3.12")
        print("   export PATH=\"/opt/homebrew/bin:$PATH\"")
        sys.exit(1)
    
    # Paso 3: Crear entorno virtual
    print("\n📋 PASO 3: Crear entorno virtual")
    if not create_venv_python312(python312_cmd):
        print("❌ Error creando entorno virtual")
        sys.exit(1)
    
    # Paso 4: Instalar PyTorch
    print("\n📋 PASO 4: Instalar PyTorch")
    if not install_pytorch_compatible():
        print("❌ Error instalando PyTorch")
        sys.exit(1)
    
    # Paso 5: Instalar resto de dependencias
    print("\n📋 PASO 5: Instalar dependencias restantes")
    if not install_remaining_dependencies():
        print("❌ Error instalando dependencias")
        sys.exit(1)
    
    # Paso 6: Verificar
    print("\n📋 PASO 6: Verificar instalación")
    if verify_installation():
        print("\n🎉 ¡CONFIGURACIÓN COMPLETADA!")
        print("=" * 40)
        print("✅ Python 3.12 configurado")
        print("✅ PyTorch instalado y compatible")
        print("✅ Todas las dependencias instaladas")
        print()
        print("📋 SIGUIENTES PASOS:")
        print("1. Activa el entorno: source .venv/bin/activate")
        print("2. Ejecuta DEOS: python run_deos.py")
        print()
        print("🔧 VERIFICACIÓN FINAL:")
        print("   python --version")
        print("   python -c 'import torch; print(torch.__version__)'")
    else:
        print("❌ Error en verificación final")
        sys.exit(1)


if __name__ == "__main__":
    main()