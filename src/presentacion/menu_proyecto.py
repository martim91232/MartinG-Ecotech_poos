from dominio.proyecto import Proyecto
from persistencia.proyecto_dao import ProyectoDAO
from datetime import datetime

def menu_proyecto():
    opcion = ""
    while opcion != "0":
        print("\n----- PROYECTOS -----")
        print("1. Registrar proyecto")
        print("2. Listar proyectos")
        print("3. Buscar proyecto")
        print("4. Actualizar proyecto")
        print("5. Eliminar proyecto")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_proyecto()
        elif opcion == "2":
            listar_proyectos()
            input("Enter para continuar")
        elif opcion == "3":
            buscar_proyecto()
        elif opcion == "4":
            actualizar_proyecto()
        elif opcion == "5":
            eliminar_proyecto()
        elif opcion == "0":
            print("Saliendo...")
        else:
            print("Opción no válida.")
            input("Presione Enter para continuar...")


def pedir_id(mensaje: str):
    try:
        return int(input(mensaje).strip())
    except ValueError:
        print("La ID debe ser un número.")
        return None


def nombre_valido(nombre: str) -> bool:
    for caracter in nombre:
        if not (caracter.isalnum() or caracter == " "):
            return False
    return True


def fecha_valida(fecha: str) -> bool:
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def registrar_proyecto():
    while True:
        nombre = input("Nombre: ").strip()
        if nombre == "":
            print("El nombre no puede estar vacío.")
            return
        if not nombre_valido(nombre):
            print("El nombre solo puede tener letras, números y espacios.")
            return
        else:
            break

    while True:
        descripcion = input("Descripcion: ").strip()
        if descripcion == "":
            print("La descripcion no puede estar vacia.")
            return
        if not nombre_valido(descripcion):
            print("La descripcion solo puede tener letras, números y espacios.")
            return
        else:
            break
        
    while True:
        fecha_inicio_str = input("Fecha de inicio (AAAA-MM-DD): ").strip()
        
        if not fecha_inicio_str:
            print("La fecha de inicio no puede estar vacía.")
            continue
            
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Formato incorrecto. Por favor, usa el formato AAAA-MM-DD (ej: 2026-10-15).")

    fecha_fin = input("Fecha de Fin (AAAA-MM-DD, Enter para omitir): ").strip()
    if fecha_fin == "":
        fecha_fin_obj = None
    elif not fecha_valida(fecha_fin):
        print("Fecha de fin no válida. Usa el formato AAAA-MM-DD.")
        input("Presione Enter para continuar...")
        return
    else:
        fecha_fin_obj = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    if fecha_fin_obj is not None and fecha_fin_obj < fecha_inicio:
        print("La fecha de fin no puede ser anterior a la fecha de inicio.")
        input("Presione Enter para continuar...")
        return

    while True:
        estado = input("Estado del proyecto: ").strip()
        if not estado.isalpha():
            print("El estado solo puede contener palabras.")
        else:
            break
    
    proyecto = Proyecto(nombre, descripcion, fecha_inicio, fecha_fin_obj, estado)
    try:
        ProyectoDAO.insertar(proyecto)
        print(f"Proyecto registrado correctamente. ID: {proyecto.id}")
    except Exception as e:
        print(f"No fue posible registrar el proyecto: {e}")
    input("Presione Enter para continuar...")


def listar_proyectos():
    print("Lista de proyectos:")
    try:
        proyectos = ProyectoDAO.listar()
        if not proyectos:
            print("No hay proyectos registrados.")
            return False
        for item in proyectos:
            print(item.mostrar_datos())
        return True
    except Exception as e:
        print(f"Error al listar los proyectos: {e}")
        return False


def buscar_proyecto():
    if not listar_proyectos():
        return
    id_proyecto = pedir_id("INGRESE LA ID DEL PROYECTO: ")
    if id_proyecto is None:
        return
    confirmacion = input("¿Está seguro de eliminarlo? (s/n): ").strip().lower()
    if confirmacion != "s":
        print("Eliminación cancelada.")
        return

    try:
        encontrado = ProyectoDAO.buscar_por_id(id_proyecto)
        if encontrado:
            print("Proyecto encontrado:")
            print(encontrado.mostrar_datos())
        else:
            print("No se encontró el proyecto.")
    except Exception as e:
        print(f"Error al buscar el proyecto: {e}")


def actualizar_proyecto():
    if not listar_proyectos():
        return
    id_proyecto = pedir_id("INGRESE LA ID DEL PROYECTO: ")
    if id_proyecto is None:
        return

    nombre_nuevo = input("Nombre nuevo: ").strip()
    if nombre_nuevo == "":
        print("El nombre no puede estar vacío.")
        return
    if not nombre_valido(nombre_nuevo):
        print("El nombre solo puede tener letras, números y espacios.")
        return

    fecha_nueva = input("Fecha de inicio nueva (AAAA-MM-DD, Enter para omitir): ").strip()
    if fecha_nueva == "":
        fecha_nueva = None
    elif not fecha_valida(fecha_nueva):
        print("Fecha no válida. Usa el formato AAAA-MM-DD.")
        return

    try:
        actualizado = ProyectoDAO.actualizar(
            Proyecto(id=id_proyecto, nombre=nombre_nuevo, fecha_inicio=fecha_nueva)
        )
        if actualizado:
            print("Proyecto actualizado correctamente.")
        else:
            print("No se encontró el proyecto.")
    except Exception as e:
        print(f"Error al actualizar el proyecto: {e}")


def eliminar_proyecto():
    if not listar_proyectos():
        return
    print("Eliminar proyecto")
    id_proyecto = pedir_id("INGRESE LA ID DEL PROYECTO: ")
    if id_proyecto is None:
        return

    try:
        eliminado = ProyectoDAO.eliminar(id_proyecto)
        if eliminado:
            print("Proyecto eliminado correctamente.")
        else:
            print("No se encontró el proyecto.")
    except Exception as e:
        print(f"Error al eliminar el proyecto: {e}")