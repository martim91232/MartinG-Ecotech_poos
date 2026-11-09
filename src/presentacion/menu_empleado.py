from dominio.empleado import Empleado
from persistencia.departamento_dao import DepartamentoDAO
from entradas import limpiar_consola, pedir_dato
from persistencia.empleado_dao import EmpleadoDAO
from servicios.autenticacion import registrar_usuario
from presentacion.menu_departamento import listar_departamentos
from persistencia.departamento_dao import DepartamentoDAO



def menu_empleados():
    opcion = ""
    while opcion != "0":
        limpiar_consola()
        print("\n------------------------------")
        print("----- EMPLEADOS -----")
        print("------------------------------")
        print("1. Registrar empleado")
        print("2. Listar empleados")
        print("3. Buscar empleado")
        print("4. Actualizar empleado")
        print("5. Eliminar empleado")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_empleado()
        elif opcion == "2":
            listar_empleados()
            input("Enter para continuar")
        elif opcion == "3":
            buscar_empleado()
        elif opcion == "4":
            actualizar_empleado()
        elif opcion == "5":
            eliminar_empleado()
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

def mostrar_departamentos():
    try:
        departamentos = DepartamentoDAO.listar()
        if not departamentos:
            print("No hay departamentos registrados.")
            input("Enter para continuar")
            return False
        print("Departamentos disponibles:")
        for item in departamentos:
            print(item.mostrar_datos())
        return True
    except Exception as e:
        print(f"Error al listar los departamentos: {e}")
        input("Presione Enter para continuar...")
        return False

def registrar_empleado():
    nombre = pedir_dato(
        "Nombre (0 para regresar): ",
        Empleado.validar_nombre,
        permitir_regreso=True,
    )
    if nombre is None:
        return

    correo = pedir_dato(
        "Correo (0 para regresar): ",
        Empleado.validar_correo,
        permitir_regreso=True,
    )
    if correo is None:
        return

    id_departamento = None
    if mostrar_departamentos():
        texto = input("ID del departamento (Enter para omitir): ").strip()
        if texto:
            try:
                id_departamento = int(texto)
            except ValueError:
                print("La ID debe ser un número.")
                input("------------------------------\nPresione Enter para continuar...\n")
                return

    try:
        if id_departamento is not None:
            if DepartamentoDAO.buscar_por_id(id_departamento) is None:
                print("No existe un departamento con esa ID.")
                input("------------------------------\nPresione Enter para continuar...\n")
                return

        empleado = Empleado(nombre, correo, id_departamento=id_departamento)
        EmpleadoDAO.insertar(empleado)
        nombre_usuario = correo.split("@", 1)[0].replace(".", "_")
        try:
            registrar_usuario(
                empleado.id,
                nombre_usuario,
                "Empleado123*",
                rol="empleado",
            )
        except (TypeError, ValueError) as error:
            print(
                f"Empleado registrado correctamente, pero no se pudo crear "
                f"su cuenta: {error}"
            )
        else:
            print(
                f"Empleado registrado correctamente. ID: {empleado.id}. "
                "Cuenta creada con la contraseña inicial Empleado123*."
            )
    except Exception as e:
        print(f"No fue posible registrar el empleado: {e}")
    input("------------------------------\nPresione Enter para continuar...\n")


def listar_empleados():
    print("Lista de empleados:")
    try:
        empleados = EmpleadoDAO.listar()
        if not empleados:
            print("No hay empleados registrados.")
            return
        for item in empleados:
            print(item.mostrar_datos())
    except Exception as e:
        print(f"Error al listar los empleados: {e}")



def buscar_empleado():
    listar_empleados()
    if not EmpleadoDAO.listar():
        input("------------------------------\nPresione Enter para continuar...\n")
        return
    id_empleado = pedir_id("INGRESE LA ID DEL EMPLEADO:")
    if id_empleado is None:
        return

    try:
        encontrado = EmpleadoDAO.buscar_por_id(id_empleado)
        if encontrado:
            print("Encontrado:", encontrado.mostrar_datos())
        else:
            print("La ID no pertenece a ningún empleado.")
    except Exception as e:
        print(f"Error al buscar el empleado: {e}")
    input("------------------------------\nPresione Enter para continuar...\n")


def actualizar_empleado():
    listar_empleados()
    if not EmpleadoDAO.listar():
        input("------------------------------\nPresione Enter para continuar...\n")
        return
    id_empleado = pedir_id("INGRESE LA ID DEL EMPLEADO: ")
    if id_empleado is None:
        return

    empleado = EmpleadoDAO.buscar_por_id(id_empleado)
    if empleado is None:
        print("No se encontró el empleado.")
        input("------------------------------\nPresione Enter para continuar...\n")
        return

    nombre_nuevo = pedir_dato(
        "Nombre nuevo (0 para regresar): ",
        Empleado.validar_nombre,
        permitir_regreso=True,
    )
    if nombre_nuevo is None:
        return
    correo_nuevo = pedir_dato(
        "Correo nuevo (0 para regresar): ",
        Empleado.validar_correo,
        permitir_regreso=True,
    )
    if correo_nuevo is None:
        return

    try:
        empleado.nombre = nombre_nuevo
        empleado.correo = correo_nuevo

        if EmpleadoDAO.actualizar(empleado):
            print("Empleado actualizado correctamente.")
        else:
            print("No se encontró el empleado.")
    except Exception as e:
        print(f"Error al actualizar el empleado: {e}")
    input("------------------------------\nPresione Enter para continuar...\n")


def eliminar_empleado():
    listar_empleados()
    if not EmpleadoDAO.listar():
        input("------------------------------\nPresione Enter para continuar...\n")
        return
    print("Eliminar empleado")
    id_empleado = pedir_id("INGRESE LA ID DEL EMPLEADO: ")
    if id_empleado is None:
        return
    confirmacion = input("¿Está seguro de eliminarlo? (s/n): ").strip().lower()
    if confirmacion != "s":
        print("Eliminación cancelada.")
        input("------------------------------\nPresione Enter para continuar...\n")
        return

    try:
        eliminado = EmpleadoDAO.eliminar(id_empleado)
        if eliminado:
            print("Empleado eliminado correctamente.")
        else:
            print("No se encontró el empleado.")
    except Exception as e:
        print(f"Error al eliminar el empleado: {e}")
    input("------------------------------\nPresione Enter para continuar...\n")
