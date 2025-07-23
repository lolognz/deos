#!/bin/bash

echo "🔧 Arreglando compatibilidad con Python 3.8..."

# Arreglar imports de typing en todos los archivos
find app/ -name "*.py" -exec sed -i '' 's/-> tuple\[/-> Tuple[/g' {} \;
find app/ -name "*.py" -exec sed -i '' 's/: tuple\[/: Tuple[/g' {} \;
find app/ -name "*.py" -exec sed -i '' 's/-> list\[/-> List[/g' {} \;
find app/ -name "*.py" -exec sed -i '' 's/: list\[/: List[/g' {} \;
find app/ -name "*.py" -exec sed -i '' 's/-> dict\[/-> Dict[/g' {} \;
find app/ -name "*.py" -exec sed -i '' 's/: dict\[/: Dict[/g' {} \;

# Agregar imports necesarios al inicio de archivos que los necesiten
for file in app/services/downloader.py app/api/*.py app/services/*.py; do
    if [ -f "$file" ]; then
        if grep -q "Tuple\|List\|Dict" "$file" && ! grep -q "from typing import" "$file"; then
            # Crear archivo temporal con el import
            echo "from typing import Tuple, List, Dict, Optional" > temp_file
            cat "$file" >> temp_file
            mv temp_file "$file"
        fi
    fi
done

echo "✅ Compatibilidad Python 3.8 arreglada"

# Arreglar script setup_deos.sh para macOS
if [ -f "setup_deos.sh" ]; then
    sed -i '' 's/timeout 10/gtimeout 10 2>\/dev\/null ||/g' setup_deos.sh
    echo "✅ Script setup_deos.sh arreglado para macOS"
fi

echo "🎉 Todos los arreglos aplicados"