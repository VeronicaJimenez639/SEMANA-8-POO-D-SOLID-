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
        """
        Ejecuta el script con el Python del entorno actual.

        ¿Por qué sys.executable?
        - Para que se ejecute con el mismo Python con el que estás ejecutando tu proyecto.
          (Por ejemplo, si estás usando un entorno virtual)

        En Windows:
        - Se abre una ventana CMD y se mantiene abierta para ver la salida.
        En otros sistemas:
        - Se ejecuta normalmente (en segundo plano).
        """
        # Python del entorno actual (más seguro que poner "python" a mano)
        python_exe = sys.executable

        # En Windows (os.name == "nt") usamos cmd /k para que la consola se quede abierta
        if os.name == "nt":
            subprocess.Popen(["cmd", "/k", python_exe, str(ruta_script)])
        else:
            # En Linux/Mac se ejecuta con el intérprete actual
            subprocess.Popen([python_exe, str(ruta_script)])

