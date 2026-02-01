"""
Archivo: script_service.py

Descripción:
Este servicio se encarga de dos cosas:
1) leer el contenido de un script .py para mostrarlo en pantalla
2) ejecutar ese script usando el Python del entorno actual
"""

import os
import subprocess
import sys
from pathlib import Path


class ScriptService:
    """Servicio para leer y ejecutar scripts de Python (.py)."""

    def leer_codigo(self, ruta_script: Path) -> str:
        """Lee el archivo .py y devuelve su contenido como texto."""
        if not ruta_script.exists():
            raise FileNotFoundError("El archivo no se encontró.")

        return ruta_script.read_text(encoding="utf-8", errors="replace")

    def ejecutar(self, ruta_script: Path) -> None:
        """Ejecuta el script con el Python del entorno actual."""
        python_exe = sys.executable              # ruta del Python que está usando este proyecto
        script_path = str(ruta_script)          # convierto Path a string para subprocess

        if os.name == "nt":  # Windows
            # Abre una consola nueva y ejecuta el script (evita problemas con espacios en rutas)
            subprocess.Popen(
                [python_exe, script_path],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:  # Linux / Mac
            subprocess.Popen([python_exe, script_path])

