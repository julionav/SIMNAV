"Script para generar archivos de python a partir de los ui encontrados en la carpeta ui"

from pathlib import Path
import subprocess

current_folder = Path(__file__).parent
ui_folder = current_folder / 'ui'

for design_path in ui_folder.iterdir():
    # Llama a pyuic5 por cada archivo ui en la carpeta ui
    subprocess.run(['pyuic5', design_path, '-o',
                    current_folder / design_path.with_suffix('.py').name])
