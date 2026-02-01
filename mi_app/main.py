"""
main.py

Este archivo arranca el programa y maneja el menú en consola.
main.py SOLO controla el flujo (mostrar opciones y leer lo que el usuario elige).
La lógica de explorar carpetas y leer/ejecutar scripts está en los servicios.
"""

from pathlib import Path  # para trabajar con rutas sin depender de strings

from modelos.recursos import UnidadCurso, SubCarpeta, ScriptPython  # modelos (solo datos)
from servicios.explorador_proyecto import ExploradorProyecto  # lista unidades/subcarpetas/scripts
from servicios.script_service import ScriptService  # lee y ejecuta scripts .py


class VolverMenuPrincipal(Exception):
    """Excepción usada solo para volver rápido al menú principal."""


def seleccionar(items: list, opcion: str):
    """
    Toma la opción del usuario (por ejemplo "1") y devuelve el elemento correspondiente.
    Si la opción no es válida, devuelve None.
    """
    try:
        idx = int(opcion) - 1  # convierto "1"->0, "2"->1, etc. (índices en Python empiezan en 0)
        if 0 <= idx < len(items):  # reviso que el índice exista dentro de la lista
            return items[idx]  # devuelvo el elemento seleccionado (unidad/carpeta/script)
        return None  # si el número no corresponde a ninguna opción
    except ValueError:
        return None  # si el usuario escribe letras u otro valor no numérico


def menu_principal(explorador: ExploradorProyecto, script_service: ScriptService) -> None:
    """
    Muestra las unidades disponibles y permite entrar a una unidad o salir.
    """
    while True:  # se repite hasta que el usuario salga
        unidades = explorador.listar_unidades()  # pido al servicio las carpetas tipo "UNIDAD X"

        print("\nMENU PRINCIPAL - DASHBOARD")  # título del menú
        for i, u in enumerate(unidades, start=1):  # enumera desde 1 para que sea cómodo al usuario
            print(f"{i} - {u.nombre}")  # muestra el nombre de cada unidad
        print("0 - Salir")  # opción para terminar el programa

        opcion = input("Elige una unidad o '0' para salir: ").strip()  # leo la elección del usuario
        if opcion == "0":  # si el usuario eligió salir
            print("Saliendo del programa.")  # mensaje final
            break  # termino el while True

        unidad = seleccionar(unidades, opcion)  # convierto el número elegido en un objeto UnidadCurso
        if unidad is None:  # si escribió algo inválido
            print("Opción no válida.")  # aviso y vuelvo a mostrar menú
            continue  # regresa al inicio del while

        try:
            menu_subcarpetas(explorador, script_service, unidad)  # entro al submenú de esa unidad
        except VolverMenuPrincipal:
            continue  # si desde scripts pidieron volver al inicio, reinicio el menú principal


def menu_subcarpetas(explorador: ExploradorProyecto, script_service: ScriptService, unidad: UnidadCurso) -> None:
    """
    Muestra las subcarpetas dentro de la unidad elegida y permite entrar o regresar.
    """
    while True:  # se repite mientras el usuario no regrese
        carpetas = explorador.listar_subcarpetas(unidad)  # pido al servicio las subcarpetas

        print(f"\nSUBMENU - {unidad.nombre}")  # indico la unidad actual
        for i, c in enumerate(carpetas, start=1):  # enumero subcarpetas desde 1
            print(f"{i} - {c.nombre}")  # muestro el nombre de cada subcarpeta
        print("0 - Regresar")  # opción para volver al menú anterior

        opcion = input("Elige una subcarpeta o '0' para regresar: ").strip()  # leo la opción
        if opcion == "0":  # si quiere regresar
            return  # salgo de esta función y vuelvo al menú principal

        carpeta = seleccionar(carpetas, opcion)  # convierto número elegido en objeto SubCarpeta
        if carpeta is None:  # si no coincide con una opción real
            print("Opción no válida.")  # aviso
            continue  # vuelvo a mostrar las subcarpetas

        menu_scripts(explorador, script_service, carpeta)  # entro al menú de scripts de esa carpeta


def menu_scripts(explorador: ExploradorProyecto, script_service: ScriptService, carpeta: SubCarpeta) -> None:
    """
    Lista los scripts .py dentro de la subcarpeta y permite:
    - ver el código
    - ejecutar el script
    - regresar o volver al menú principal
    """
    while True:  # se repite hasta regresar o volver al inicio
        scripts = explorador.listar_scripts(carpeta)  # pido al servicio los archivos .py de la carpeta

        print(f"\nSCRIPTS - {carpeta.nombre}")  # indico la carpeta actual
        for i, s in enumerate(scripts, start=1):  # enumero scripts desde 1
            print(f"{i} - {s.nombre}")  # muestro nombre del archivo
        print("0 - Regresar")  # vuelve a subcarpetas
        print("9 - Menú principal")  # vuelve al inicio (sin salir del programa)

        opcion = input("Elige un script: ").strip()  # leo la elección del usuario
        if opcion == "0":  # regresar al submenú anterior
            return  # salgo de esta función
        if opcion == "9":  # volver al menú principal
            raise VolverMenuPrincipal()  # lanzo excepción para subir directo al menú principal

        script = seleccionar(scripts, opcion)  # convierto la opción en objeto ScriptPython
        if script is None:  # si la opción no corresponde a un script
            print("Opción no válida.")  # aviso
            continue  # vuelvo a pedir

        ver_y_ejecutar(script_service, script)  # muestro el código y pregunto si ejecutar


def ver_y_ejecutar(script_service: ScriptService, script: ScriptPython) -> None:
    """
    Muestra el contenido del script y luego pregunta si se desea ejecutarlo.
    """
    try:
        codigo = script_service.leer_codigo(script.ruta)  # leo el archivo seleccionado como texto

        print(f"\n--- Código de {script.nombre} ---\n")  # título para separar visualmente
        print(codigo)  # imprimo el código completo en consola

        ejecutar = input("\n¿Desea ejecutar el script? (1: Sí, 0: No): ").strip()  # pregunto decisión
        if ejecutar == "1":  # si el usuario acepta
            script_service.ejecutar(script.ruta)  # ejecuto el archivo (abre consola en Windows)
        else:
            print("No se ejecutó el script.")  # si no ejecuta, solo informo

    except Exception as exc:
        print(f"Error: {exc}")  # si algo falla, muestro el error sin cerrar el programa

    input("\nEnter para continuar...")  # pausa para que el usuario lea antes de volver al menú


def main() -> None:
    """
    Crea los servicios y arranca el dashboard.
    """
    ruta_base = Path(__file__).resolve().parent  # carpeta donde está este main.py (base del proyecto)
    explorador = ExploradorProyecto(ruta_base)  # servicio que sabe “buscar” carpetas y scripts
    script_service = ScriptService()  # servicio que sabe leer/ejecutar scripts

    menu_principal(explorador, script_service)  # inicio el menú principal


if __name__ == "__main__":
    main()  # punto de entrada cuando se ejecuta: python main.py  

