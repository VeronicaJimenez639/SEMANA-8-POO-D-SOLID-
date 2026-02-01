"""
Archivo: recursos.py

Descripción:
Este módulo contiene los MODELOS (clases de datos) del proyecto Dashboard.py
Su objetivo es representar, de forma ordenada, los elementos que el Dashboard muestra:

- UnidadCurso: una carpeta de unidad (ej. "UNIDAD 1")
- SubCarpeta: una carpeta dentro de una unidad (ej. "Semana_01" o "Tarea_02")
- ScriptPython: un archivo .py dentro de una subcarpeta

Importante:
Aquí NO se escribe lógica (no se listan carpetas, no se ejecuta código).
Solo se definen estructuras de datos para que los servicios y el main trabajen de forma clara.
"""

from dataclasses import dataclass
from pathlib import Path


# @dataclass permite crear clases de datos sin escribir a mano __init__, __repr__, etc.
# frozen=True hace que los objetos sean inmutables:
# Una vez creado un modelo, no se puede cambiar su nombre o ruta
# Esto evita errores y mantiene consistencia (buenas prácticas en modelos)
@dataclass(frozen=True)
class UnidadCurso:
    """
    Modelo: representa una unidad del curso.

    Ejemplo:
    - nombre: "UNIDAD 1"
    - ruta: Path("C:/.../UNIDAD 1")
    """
    nombre: str  # Nombre visible de la unidad (el nombre de la carpeta)
    ruta: Path   # Ruta completa hacia la carpeta de esa unidad


@dataclass(frozen=True)
class SubCarpeta:
    """
    Modelo: representa una subcarpeta dentro de una unidad.

    Ejemplo:
    - nombre: "Semana_01"
    - ruta: Path("C:/.../UNIDAD 1/Semana_01")
    """
    nombre: str  # Nombre visible de la subcarpeta
    ruta: Path   # Ruta completa hacia la subcarpeta


@dataclass(frozen=True)
class ScriptPython:
    """
    Modelo: representa un script de Python (.py) ubicado dentro de una subcarpeta.

    Ejemplo:
    - nombre: "ejercicio1.py"
    - ruta: Path("C:/.../UNIDAD 1/Semana_01/ejercicio1.py")
    """
    nombre: str  # Nombre del archivo (con extensión .py)
    ruta: Path   # Ruta completa hacia el archivo .py

