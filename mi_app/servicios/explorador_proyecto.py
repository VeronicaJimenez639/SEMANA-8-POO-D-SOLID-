"""
Archivo: explorador_proyecto.py

Descripción:
Este módulo contiene el servicio ExploradorProyecto.
Su función es RECORRER (explorar) las carpetas del proyecto para encontrar:

1) Unidades del curso (carpetas como "UNIDAD 1", "UNIDAD 2")
2) Subcarpetas dentro de una unidad (semanas, tareas, ejercicios, etc.)
3) Scripts de Python (.py) dentro de una subcarpeta

Importante:
- Este servicio NO muestra menús y NO pide input al usuario.
- Solo devuelve listas de modelos (UnidadCurso, SubCarpeta, ScriptPython).
- La parte de imprimir y elegir opciones se hace en main.py (la UI).

Esto aplica el principio SRP (Responsabilidad Única):
ExploradorProyecto solo explora; no hace otras tareas.
"""

from pathlib import Path
from typing import List

# Importamos los modelos (solo datos) que vamos a devolver
from modelos.recursos import UnidadCurso, SubCarpeta, ScriptPython


class ExploradorProyecto:
    """
    Servicio: se encarga de explorar carpetas del proyecto.

    ¿Qué significa "explorar" aquí?
    Significa recorrer directorios con Path para obtener información del proyecto.
    """

    def __init__(self, ruta_base: Path) -> None:
        """
        Constructor del servicio.

        ruta_base: es la ruta desde donde vamos a buscar las unidades.
        Normalmente es la raíz del proyecto (donde están 'UNIDAD 1', 'UNIDAD 2', etc.).
        """
        # Guardamos la ruta base como atributo "privado" (por convención con _)
        self._ruta_base = ruta_base

    def listar_unidades(self) -> List[UnidadCurso]:
        """
        Busca las carpetas de unidades en la raíz del proyecto.

        Regla:
        - Se considera unidad a toda carpeta cuyo nombre empiece con "UNIDAD"
          (por ejemplo: "UNIDAD 1", "UNIDAD 2").
        """
        # Creamos una lista vacía donde iremos guardando las unidades encontradas
        unidades: List[UnidadCurso] = []

        # iterdir() recorre todo lo que hay dentro de ruta_base (archivos y carpetas)
        for item in self._ruta_base.iterdir():

            # is_dir(): verifica que sea carpeta
            # item.name.upper().startswith("UNIDAD"): detecta nombres que inicien con UNIDAD,
            # sin importar si están en mayúsculas o minúsculas
            if item.is_dir() and item.name.upper().startswith("UNIDAD"):
                # Convertimos esa carpeta en un modelo UnidadCurso
                unidades.append(UnidadCurso(nombre=item.name, ruta=item))

        # sorted(...): ordena las unidades por el nombre (para que el menú salga ordenado)
        return sorted(unidades, key=lambda u: u.nombre)

    def listar_subcarpetas(self, unidad: UnidadCurso) -> List[SubCarpeta]:
        """
        Lista las subcarpetas que están dentro de una unidad.

        Ejemplo:
        unidad = "UNIDAD 1"
        subcarpetas podrían ser: "Semana_01", "Tarea_02", etc.
        """
        carpetas: List[SubCarpeta] = []

        # Recorremos todo lo que hay dentro de la ruta de la unidad
        for item in unidad.ruta.iterdir():
            # Solo nos interesan carpetas
            if item.is_dir():
                carpetas.append(SubCarpeta(nombre=item.name, ruta=item))

        # Ordenamos por nombre para mostrarlo de forma ordenada
        return sorted(carpetas, key=lambda c: c.nombre)

    def listar_scripts(self, carpeta: SubCarpeta) -> List[ScriptPython]:
        """
        Lista los archivos Python (.py) dentro de una subcarpeta.

        Ejemplo:
        carpeta = "Semana_01"
        scripts podrían ser: "ejercicio1.py", "main.py", etc.
        """
        scripts: List[ScriptPython] = []

        # Recorremos los elementos dentro de la subcarpeta
        for item in carpeta.ruta.iterdir():

            # is_file(): verifica que sea archivo
            # item.suffix == ".py": verifica que la extensión sea .py
            if item.is_file() and item.suffix == ".py":
                scripts.append(ScriptPython(nombre=item.name, ruta=item))

        # Ordenamos los scripts por nombre
        return sorted(scripts, key=lambda s: s.nombre)
