#!/usr/bin/env python3
"""
🔧 DEOS - Detector y Configurador de Python 3.9+
Script para encontrar Python 3.9+ en macOS y recrear el entorno virtual
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def find_python_versions():
    """Encuentra todas las versiones de Python disponibles en el sistema"""
    python_candidates = [
        'python3.13', 'python3.12', 'python3.11', 'python3.10', 'python3.9',
        '/usr/bin/python3', '/usr/local/bin/python3', 
        '/opt/homebrew/bin/python3', '/opt/homebrew/bin/python3.12',
        '/opt/homebrew/bin/python3.11', '/opt/homebrew/bin/python3.10',
        '/opt/homebrew/bin/python3.9',
        'python3'
    ]
    
    valid_pythons = []
    
    for candidate in python_candidates:
        try:
            result = subprocess.run([candidate, '--version'], 
                                  capture_output=True, text=True, check=True)
            version_str = result.stdout.strip()
            version_parts = version_str.split()[1].split('.')
            major, minor = int(version_parts[0]), int(version_parts[1])
            
            if major >= 3 and minor >= 9:
                # Obtener la ruta completa
                which_result = subprocess.run(['which', candidate], 
                                            capture_output=True, text=True, check=True)
                python_path = which_result.stdout.strip()
                
                valid_pythons.append({
                    'command': candidate,
                    'path': python_path,
                    'version': f"{major}.{minor}",
                    'full_version': version_str
                })
                print(f"✅ Encontrado: {candidate} -> {version_str} en {python_path}")
            else:
                print(f"❌ {candidate} -> {version_str} (muy antiguo)")
        except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
            continue
    
    return valid_pythons


def check_conda_python():
    """Verifica si conda tiene Python 3.9+ disponible"""
    try:
        # Verificar si conda está disponible
        result = subprocess.run(['conda', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Conda disponible: {result.stdout.strip()}")
        
        # Listar entornos de conda
        result = subprocess.run(['conda', 'info', '--envs'], 
                              capture_output=True, text=True, check=True)
        print("📋 Entornos conda disponibles:")
        for line in result.stdout.split('\n'):
            if line.strip() and not line.startswith('#'):
                print(f"   {line}")
        
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ℹ️  Conda no está disponible")
        return False


def suggest_python_installation():
    """Sugiere cómo instalar Python 3.9+ en macOS"""
    print("\n🔧 OPCIONES PARA INSTALAR PYTHON 3.9+:")
    print("="*50)
    
    print("\n1️⃣  VIA HOMEBREW (Recomendado):")
    print("   brew install python@3.12")
    print("   # Luego añadir a PATH: export PATH=/opt/homebrew/bin:$PATH")
    
    print("\n2️⃣  VIA CONDA:")
    print("   conda create -n deos python=3.12")
    print("   conda activate deos")
    
    print("\n3️⃣  VIA PYTHON.ORG:")
    print("   Descargar desde: https://www.python.org/downloads/")
    print("   Instalar Python 3.12.x para macOS")
    
    print("\n4️⃣  VIA PYENV:")
    print("   pyenv install 3.12.0")
    print("   pyenv global 3.12.0")


def create_venv_with_python(python_path):
    """Crea el entorno virtual con la versión específica de Python"""
    print(f"\n🔨 Creando entorno virtual con {python_path}...")
    
    # Eliminar entorno anterior
    venv_path = Path(".venv")
    if venv_path.exists():
        print("🗑️  Eliminando entorno virtual anterior...")
        shutil.rmtree(venv_path)
    
    # Crear nuevo entorno
    try:
        subprocess.run([python_path, '-m', 'venv', '.venv'], check=True)
        print("✅ Entorno virtual creado exitosamente")
        
        # Verificar la versión en el nuevo entorno
        if os.name == 'nt':
            venv_python = Path('.venv/Scripts/python.exe')
        else:
            venv_python = Path('.venv/bin/python')
        
        if venv_python.exists():
            result = subprocess.run([str(venv_python), '--version'], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ Versión en entorno virtual: {result.stdout.strip()}")
            return True
        else:
            print("❌ Error: No se pudo verificar el entorno virtual")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando entorno virtual: {e}")
        return False


def install_dependencies():
    """Instala dependencias en el nuevo entorno virtual"""
    venv_python = Path('.venv/bin/python')
    
    if not venv_python.exists():
        print("❌ No se encontró Python en el entorno virtual")
        return False
    
    print("📦 Instalando dependencias...")
    
    # Actualizar pip
    try:
        subprocess.run([str(venv_python), '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      check=True)
        print("✅ pip actualizado")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Advertencia: Error actualizando pip: {e}")
    
    # Instalar dependencias
    try:
        subprocess.run([str(venv_python), '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ Dependencias instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False


def main():
    """Función principal"""
    print("🔍 DEOS - Detector de Python 3.9+")
    print("="*40)
    
    # Verificar directorio
    if not Path("app/main.py").exists():
        print("❌ Error: Ejecuta desde el directorio raíz de DEOS")
        sys.exit(1)
    
    print("\n🔍 Buscando versiones de Python en el sistema...")
    valid_pythons = find_python_versions()
    
    if not valid_pythons:
        print("\n❌ No se encontró Python 3.9+ en el sistema")
        check_conda_python()
        suggest_python_installation()
        
        print("\n💡 SOLUCIÓN RÁPIDA:")
        print("1. Instala Python 3.12: brew install python@3.12")
        print("2. Ejecuta este script de nuevo")
        sys.exit(1)
    
    # Mostrar opciones disponibles
    print(f"\n✅ Encontradas {len(valid_pythons)} versiones compatibles:")
    for i, python_info in enumerate(valid_pythons, 1):
        print(f"   {i}. {python_info['full_version']} ({python_info['path']})")
    
    # Usar la primera (más reciente) automáticamente
    selected_python = valid_pythons[0]
    print(f"\n🎯 Usando: {selected_python['full_version']} ({selected_python['path']})")
    
    # Crear entorno virtual
    if create_venv_with_python(selected_python['path']):
        print("\n📦 Instalando dependencias...")
        if install_dependencies():
            print("\n🎉 ¡CONFIGURACIÓN COMPLETADA!")
            print("="*40)
            print(f"✅ Entorno virtual creado con Python {selected_python['full_version']}")
            print("✅ Dependencias instaladas")
            print("\n📋 SIGUIENTES PASOS:")
            print("1. Activa el entorno: source .venv/bin/activate")
            print("2. Ejecuta DEOS: python run_deos.py")
            
            # También verificar conda
            check_conda_python()
        else:
            print("❌ Error instalando dependencias")
            sys.exit(1)
    else:
        print("❌ Error creando entorno virtual")
        sys.exit(1)


if __name__ == "__main__":
    main()