# Dashboard POO (Semana 8) – Refactor con SOLID

## Descripción
Este proyecto es una adaptación del archivo `Dashboard.py` del repositorio de la materia.  
El objetivo es tener un **dashboard en consola** que permita:
- listar **unidades** (carpetas `UNIDAD 1`, `UNIDAD 2`, etc.)
- entrar a **subcarpetas**
- ver el **código** de scripts `.py`
- **ejecutar** los scripts seleccionados

La refactorización se realizó usando la arquitectura **modelos / servicios / main.py**, aplicando buenas prácticas e idea de principios **SOLID**.

---

## Estructura del proyecto
Dentro de `mi_app/` se organiza así:

- `modelos/`
  - `recursos.py`: clases que representan datos (Unidad, SubCarpeta, Script)
- `servicios/`
  - `explorador_proyecto.py`: recorre carpetas y lista unidades/subcarpetas/scripts
  - `script_service.py`: lee el contenido de un `.py` y lo ejecuta con Python
- `main.py`
  - maneja el menú (interfaz en consola) y usa los servicios

---

## Cómo ejecutar
1. Entra a la carpeta del proyecto.
2. Ejecuta:

```bash
cd mi_app
python main.py
