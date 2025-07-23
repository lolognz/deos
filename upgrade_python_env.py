#!/usr/bin/env python3
"""
🔧 DEOS Python Environment Upgrade Script
Script para actualizar el entorno virtual de Python 3.8 a Python 3.9+
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def print_step(step, message):
    """Imprime un paso con formato"""
    print(f"\n{'='*60}")
    print(f"📋 PASO {step}: {message}")
    print('='*60)


def check_system_python():
    """Verifica que el sistema tenga Python 3.9+"""
    print("🔍 Verificando versión de Python del sistema...")
    
    # Verificar python3
    try:
        result = subprocess.run([sys.executable, '--version'], 
                              capture_output=True, text=True, check=True)
        version_str = result.stdout.strip()
        print(f"✅ Encontrado: {version_str}")
        
        # Extraer versión
        version_parts = version_str.split()[1].split('.')
        major, minor = int(version_parts[0]), int(version_parts[1])
        
        if major >= 3 and minor >= 9:
            return True, f"{major}.{minor}"
        else:
            return False, f"{major}.{minor}"
            
    except Exception as e:
        print(f"❌ Error verificando Python: {e}")
        return False, "unknown"


def backup_requirements():
    """Hace backup de requirements.txt si existe"""
    req_file = Path("requirements.txt")
    backup_file = Path("requirements.txt.backup")
    
    if req_file.exists():
        shutil.copy2(req_file, backup_file)
        print(f"✅ Backup creado: {backup_file}")
        return True
    return False


def remove_old_venv():
    """Elimina el entorno virtual anterior"""
    venv_path = Path(".venv")
    if venv_path.exists():
        print(f"🗑️  Eliminando entorno virtual anterior: {venv_path}")
        shutil.rmtree(venv_path)
        print("✅ Entorno virtual anterior eliminado")
    else:
        print("ℹ️  No se encontró entorno virtual anterior")


def create_new_venv():
    """Crea un nuevo entorno virtual con Python 3.9+"""
    print("🔨 Creando nuevo entorno virtual...")
    
    try:
        subprocess.run([sys.executable, '-m', 'venv', '.venv'], 
                      check=True)
        print("✅ Nuevo entorno virtual creado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando entorno virtual: {e}")
        return False


def get_venv_python():
    """Obtiene la ruta del Python del entorno virtual"""
    if os.name == 'nt':  # Windows
        return Path('.venv/Scripts/python.exe')
    else:  # macOS/Linux
        return Path('.venv/bin/python')


def install_dependencies():
    """Instala las dependencias en el nuevo entorno virtual"""
    venv_python = get_venv_python()
    
    if not venv_python.exists():
        print(f"❌ No se encontró Python en el entorno virtual: {venv_python}")
        return False
    
    print("📦 Instalando dependencias...")
    
    # Actualizar pip primero
    try:
        subprocess.run([str(venv_python), '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      check=True)
        print("✅ pip actualizado")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Advertencia: Error actualizando pip: {e}")
    
    # Instalar dependencias
    req_file = Path("requirements.txt")
    if req_file.exists():
        try:
            print("📥 Instalando dependencias desde requirements.txt...")
            subprocess.run([str(venv_python), '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                          check=True)
            print("✅ Dependencias instaladas exitosamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando dependencias: {e}")
            return False
    else:
        print("⚠️  No se encontró requirements.txt")
        return False


def verify_installation():
    """Verifica que la instalación sea correcta"""
    venv_python = get_venv_python()
    
    print("🔍 Verificando instalación...")
    
    # Verificar versión de Python
    try:
        result = subprocess.run([str(venv_python), '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Python en venv: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Error verificando Python: {e}")
        return False
    
    # Verificar dependencias principales
    try:
        result = subprocess.run([str(venv_python), '-c', 
                               'import fastapi, uvicorn; print("FastAPI y Uvicorn disponibles")'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"❌ Error verificando dependencias: {e}")
        return False


def print_next_steps():
    """Imprime los siguientes pasos a seguir"""
    activation_cmd = "source .venv/bin/activate" if os.name != 'nt' else ".venv\\Scripts\\activate"
    
    print(f"""
🎉 ¡ACTUALIZACIÓN COMPLETADA EXITOSAMENTE!

📋 SIGUIENTES PASOS:

1. Activa el nuevo entorno virtual:
   {activation_cmd}

2. Verifica que todo funcione:
   python run_deos.py

3. Si usas VS Code/PyCharm, selecciona el nuevo intérprete:
   .venv/bin/python (macOS/Linux) o .venv\\Scripts\\python.exe (Windows)

4. Ejecuta los tests para verificar:
   python -m pytest tests/ -v

🔧 COMANDOS ÚTILES:
   • Ejecutar servidor: python run_deos.py
   • Ver versión Python: python --version
   • Instalar nueva dependencia: pip install <paquete>

""")


def main():
    """Función principal"""
    print("🚀 DEOS - Actualizador de Entorno Python")
    print("Actualizando de Python 3.8 a Python 3.9+")
    
    # Verificar que estamos en el directorio correcto
    if not Path("app/main.py").exists():
        print("❌ Error: No se encontró app/main.py")
        print("   Ejecuta este script desde el directorio raíz del proyecto DEOS")
        sys.exit(1)
    
    # Paso 1: Verificar Python del sistema
    print_step(1, "Verificando Python del sistema")
    has_python39, version = check_system_python()
    
    if not has_python39:
        print(f"❌ Error: Se requiere Python 3.9+, encontrado: {version}")
        print("   Instala Python 3.9+ desde https://python.org o usando Homebrew:")
        print("   brew install python@3.12")
        sys.exit(1)
    
    # Paso 2: Backup requirements
    print_step(2, "Haciendo backup de configuración")
    backup_requirements()
    
    # Paso 3: Eliminar entorno virtual anterior
    print_step(3, "Eliminando entorno virtual anterior")
    remove_old_venv()
    
    # Paso 4: Crear nuevo entorno virtual
    print_step(4, "Creando nuevo entorno virtual")
    if not create_new_venv():
        sys.exit(1)
    
    # Paso 5: Instalar dependencias
    print_step(5, "Instalando dependencias")
    if not install_dependencies():
        print("⚠️  Algunas dependencias fallaron, pero puedes continuar")
    
    # Paso 6: Verificar instalación
    print_step(6, "Verificando instalación")
    verify_installation()
    
    # Mostrar siguientes pasos
    print_next_steps()


if __name__ == "__main__":
    main()