#!/usr/bin/env python3
"""
🔧 DEOS - Solucionador de Warning de NumPy
Script opcional para eliminar el warning de NumPy 2.x
"""

import subprocess
import sys
from pathlib import Path


def fix_numpy_warning():
    """Arregla el warning de NumPy instalando una versión compatible"""
    print("🔧 Solucionando warning de NumPy...")
    print("   El warning no afecta la funcionalidad, pero es molesto visualmente")
    
    # Verificar que estamos en el entorno virtual
    venv_python = Path('.venv/bin/python')
    if not venv_python.exists():
        print("❌ Error: No se encontró entorno virtual .venv")
        print("   Ejecuta este script desde el directorio raíz de DEOS")
        return False
    
    try:
        # Downgrade a NumPy 1.x
        print("📦 Instalando NumPy 1.x compatible...")
        subprocess.run([
            str(venv_python), '-m', 'pip', 'install', 
            'numpy>=1.21.0,<2.0.0', '--force-reinstall'
        ], check=True)
        
        print("✅ NumPy downgradeado exitosamente")
        print("   El warning de NumPy 2.x debería desaparecer")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando NumPy: {e}")
        return False


def verify_fix():
    """Verifica que el fix funcione"""
    venv_python = Path('.venv/bin/python')
    
    try:
        result = subprocess.run([
            str(venv_python), '-c', 
            'import numpy; print(f"NumPy version: {numpy.__version__}")'
        ], capture_output=True, text=True, check=True)
        
        print(f"✅ {result.stdout.strip()}")
        
        # Verificar que PyTorch sigue funcionando
        result = subprocess.run([
            str(venv_python), '-c', 
            'import torch; print(f"PyTorch version: {torch.__version__}")'
        ], capture_output=True, text=True, check=True)
        
        print(f"✅ {result.stdout.strip()}")
        print("✅ Todas las dependencias siguen funcionando")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error verificando: {e}")
        return False


def main():
    """Función principal"""
    print("🔧 DEOS - Solucionador de Warning de NumPy")
    print("=" * 45)
    
    if not Path("app/main.py").exists():
        print("❌ Error: Ejecuta desde el directorio raíz de DEOS")
        sys.exit(1)
    
    print("\n📋 Este script eliminará el warning:")
    print('   "A module that was compiled using NumPy 1.x cannot be run in NumPy 2.1.2"')
    print("\n⚠️  NOTA: El warning no afecta la funcionalidad de DEOS")
    print("   Solo es cosmético. ¿Quieres continuar? (y/N): ", end="")
    
    respuesta = input().lower().strip()
    
    if respuesta not in ['y', 'yes', 'sí', 'si']:
        print("❌ Operación cancelada")
        sys.exit(0)
    
    print("\n🔧 Procediendo con el fix...")
    
    if fix_numpy_warning():
        print("\n🔍 Verificando fix...")
        if verify_fix():
            print("\n🎉 ¡Warning solucionado exitosamente!")
            print("   Reinicia DEOS para ver los cambios")
        else:
            print("❌ Error en verificación")
    else:
        print("❌ Error aplicando fix")


if __name__ == "__main__":
    main()