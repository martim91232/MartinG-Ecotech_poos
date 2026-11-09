from dominio.proyecto import Proyecto
from persistencia.proyecto_dao import ProyectoDAO
from datetime import datetime
from entradas import limpiar_consola, pedir_dato

def menu_proyecto():
    opcion = ""
    while opcion != "0":
        limpiar_consola()
        print("\n------------------------------")
        print("----- PROYECTOS -----")
        print("------------------------------")
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
            input("------------------------------\nPresione Enter para continuar...\n")


def pedir_id(mensaje: str):
    try:
        texto = input(f"{mensaje} (0 para regresar)").strip()
        if texto == "0":
            return None
        valor = int(texto)
        if not 1 <= valor <= 9223372036854775807:
            raise ValueError
        return valor
    except ValueError:
        print("Ingresa una ID válida dentro del rango permitido.")
        input("------------------------------\nPresione Enter para continuar...\n")
        return None


def nombre_valido(nombre: str) -> bool:
    return bool(nombre and nombre.strip() and all(
        caracter.isalnum() or caracter == " "
        for caracter in nombre
    ))


def validar_texto_proyecto(texto, campo):
    if not isinstance(texto, str):
        raise TypeError(f"{campo} debe ser texto.")
    texto = texto.strip()
    if not texto:
        raise ValueError(f"{campo} no puede estar vacío.")
    if not nombre_valido(texto):
        raise ValueError(
            f"{campo} solo puede tener letras, números y espacios."
        )
    return texto


def validar_estado(estado):
    estado = validar_texto_proyecto(estado, "El estado")
    if not all(caracter.isalpha() or caracter == " " for caracter in estado):
        raise ValueError("El estado solo puede contener palabras.")
    return estado


def fecha_valida(fecha: str) -> bool:
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def registrar_proyecto():
    nombre = pedir_dato(
        "Nombre (0 para regresar): ",
        lambda valor: validar_texto_proyecto(valor, "El nombre"),
        permitir_regreso=True,
    )
    if nombre is None:
        return

    descripcion = pedir_dato(
        "Descripción (0 para regresar): ",
        lambda valor: validar_texto_proyecto(valor, "La descripción"),
        permitir_regreso=True,
    )
    if descripcion is None:
        return
        
    while True:
        fecha_inicio_str = input(
            "Fecha de inicio (AAAA-MM-DD, 0 para regresar): "
        ).strip()
        if fecha_inicio_str == "0":
            return
        
        if not fecha_inicio_str:
            print("La fecha de inicio no puede estar vacía.")
            input("Presione Enter para continuar...")
            continue
            
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Formato incorrecto. Por favor, usa el formato AAAA-MM-DD (ej: 2026-10-15).")
            input("Presione Enter para continuar...")

    fecha_fin = input(
        "Fecha de Fin (AAAA-MM-DD, Enter para omitir, 0 para regresar): "
    ).strip()
    if fecha_fin == "0":
        return
    if fecha_fin == "":
        fecha_fin_obj = None
    elif not fecha_valida(fecha_fin):
        print("Fecha de fin no válida. Usa el formato AAAA-MM-DD.")
        input("------------------------------\nPresione Enter para continuar...\n")
        return
    else:
        fecha_fin_obj = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    if fecha_fin_obj is not None and fecha_fin_obj < fecha_inicio:
        print("La fecha de fin no puede ser anterior a la fecha de inicio.")
        input("------------------------------\nPresione Enter para continuar...\n")
        return

    estado = pedir_dato(
        "Estado del proyecto (0 para regresar): ",
        validar_estado,
        permitir_regreso=True,
    )
    if estado is None:
        return
    
    proyecto = Proyecto(nombre, descripcion, fecha_inicio, fecha_fin_obj, estado)
    try:
        ProyectoDAO.insertar(proyecto)
        print(f"Proyecto registrado correctamente. ID: {proyecto.id}")
    except Exception as e:
        print(f"No fue posible registrar el proyecto: {e}")
    input("------------------------------\nPresione Enter para continuar...\n")


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
        input("------------------------------\nPresione Enter para continuar...\n")
        return
    id_proyecto = pedir_id("INGRESE LA ID DEL PROYECTO: ")
    if id_proyecto is None:
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
    input("------------------------------\nPresione Enter para continuar...\n")


def actualizar_proyecto():
    if not listar_proyectos():
        input("------------------------------\nPresione Enter para continuar...\n")
        return
    id_proyecto = pedir_id("INGRESE LA ID DEL PROYECTO: ")
    if id_proyecto is None:
        return

    if ProyectoDAO.buscar_por_id(id_proyecto) is None:
        print("No se encontró el proyecto.")
        input("------------------------------\nPresione Enter para continuar...\n")
        return

    nombre_nuevo = input("Nombre nuevo (0 para regresar): ").strip()
    if nombre_nuevo == "0":
        return
    if nombre_nuevo == "":
        print("El nombre no puede estar vacío.")
        input("------------------------------\nPresione Enter para continuar...\n")
        return
    if not nombre_valido(nombre_nuevo):
        print("El nombre solo puede tener letras, números y espacios.")
        input("------------------------------\nPresione Enter para continuar...\n")
        return

    fecha_nueva = input(
        "Fecha de inicio nueva (AAAA-MM-DD, Enter para omitir, 0 para regresar): "
    ).strip()
    if fecha_nueva == "0":
        return
    if fecha_nueva == "":
        fecha_nueva = None
    elif not fecha_valida(fecha_nueva):
        print("Fecha no válida. Usa el formato AAAA-MM-DD.")
        input("------------------------------\nPresione Enter para continuar...\n")
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
    input("------------------------------\nPresione Enter para continuar...\n")


def eliminar_proyecto():
    if not listar_proyectos():
        input("------------------------------\nPresione Enter para continuar...\n")
        return
    print("Eliminar proyecto")
    id_proyecto = pedir_id("INGRESE LA ID DEL PROYECTO: ")
    if id_proyecto is None:
        return
    confirmacion = input("¿Está seguro de eliminarlo? (s/n): ").strip().lower()
    if confirmacion != "s":
        print("Eliminación cancelada.")
        input("------------------------------\nPresione Enter para continuar...\n")
        return

    try:
        eliminado = ProyectoDAO.eliminar(id_proyecto)
        if eliminado:
            print("Proyecto eliminado correctamente.")
        else:
            print("No se encontró el proyecto.")
    except Exception as e:
        print(f"Error al eliminar el proyecto: {e}")
    input("------------------------------\nPresione Enter para continuar...\n")