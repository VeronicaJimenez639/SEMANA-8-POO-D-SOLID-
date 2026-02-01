"""
Archivo: script_service.py

Descripción:
Este módulo contiene el servicio ScriptService.
Su objetivo es manejar acciones relacionadas con archivos Python (.py), específicamente:

1) leer_codigo(): leer el contenido de un script y devolverlo como texto
2) ejecutar(): ejecutar un script usando el Python del entorno actual

Importante:
- Este servicio NO imprime menús ni pide opciones al usuario.
- Solo ofrece funciones para que main.py (la interfaz) decida qué mostrar y qué ejecutar.
"""

import os
import subprocess
import sys
from pathlib import Path


class ScriptService:
    """
    Servicio para trabajar con scripts Python.

    Aquí colocamos la lógica de:
    - leer un archivo .py
    - ejecutar un archivo .py

    Esto ayuda a separar responsabilidades:
    main.py se encarga del menú (UI) y este servicio se encarga de la acción.
    """

    def leer_codigo(self, ruta_script: Path) -> str:
        """
        Lee el contenido del script y lo devuelve como texto.

        Parámetro:
        - ruta_script: ruta completa del archivo .py

        Retorna:
        - El contenido del archivo como string (texto).
        """
        # Verificamos que el archivo exista para evitar errores al leerlo
        if not ruta_script.exists():
            raise FileNotFoundError("El archivo no se encontró.")

        # read_text lee el archivo completo
        # encoding="utf-8" ayuda con caracteres especiales (tildes)
        # errors="replace" evita que el programa se caiga si hay algún símbolo raro
        return ruta_script.read_text(encoding="utf-8", errors="replace")
    

    def ejecutar(self, ruta_script: Path) -> None:
    python_exe = sys.executable  # Python del entorno actual (el mismo que usa tu proyecto)
    script_path = str(ruta_script)  # convierto Path a texto para pasarlo a subprocess

    if os.name == "nt":  # si es Windows
        subprocess.Popen(
            [python_exe, script_path],  # ejecuta: python script.py (sin cmd, evita problemas por espacios)
            creationflags=subprocess.CREATE_NEW_CONSOLE  # abre una consola nueva para ver la salida
        )
    else:  # Linux / Mac
        subprocess.Popen([python_exe, script_path])  # ejecuta normal


