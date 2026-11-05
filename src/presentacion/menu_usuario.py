from getpass import getpass
from entradas import pedir_dato, limpiar_consola
from servicios.autenticacion import (
    autenticar,
    autenticar_empleado,
    registrar_usuario,
)
from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO
from servicios.permisos import exigir_admin, exigir_sesion
from servicios.mi_cuenta import (
    mi_ficha,
    mi_registros,
    mi_departamento,
    actualizar_mis_datos,
)
from servicios.indicadores import obtener_datos, extraer_clp
from servicios.gestion_empleado import listar_todos
import requests


def solicitar_registro():
    try:
        usuarios = UsuarioDAO.listar()
        empleados_con_cuenta = {usuario.empleado_id for usuario in usuarios}
        empleados = [
            empleado for empleado in EmpleadoDAO.listar()
            if empleado.id not in empleados_con_cuenta
        ]
        if not empleados:
            print("No hay empleados disponibles para registrar.")
            input("Presione Enter para continuar...")
            return None

        print("Empleados disponibles:")
        for empleado in empleados:
            print(f"ID: {empleado.id} - {empleado.nombre}")

        print("0. Regresar")
        empleado_texto = input("ID del empleado (0 para regresar): ").strip()
        if empleado_texto == "0":
            return None
        try:
            empleado_id = int(empleado_texto)
        except ValueError:
            print("Ingresa una ID válida.")
            input("Presione Enter para continuar...")
            return None

        if EmpleadoDAO.buscar_por_id(empleado_id) is None:
            raise ValueError("No existe un empleado con ese ID.")
        if empleado_id in empleados_con_cuenta:
            raise ValueError("El empleado ya tiene una cuenta registrada.")

        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass)

        if clave != getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden. Vuelva al registro.")
            input("Presione Enter para continuar...")
            return None

        usuario_id = registrar_usuario(empleado_id, nombre, clave)
    except (TypeError, ValueError) as error:
        print(error)
        input("Presione Enter para continuar...")
        return None

    print(f"Cuenta creada correctamente. ID: {usuario_id}")
    return usuario_id


def solicitar_login():
    print("\n------------------------------")
    print("1. Iniciar como administrador")
    print("2. Iniciar como empleado")
    print("0. Regresar")
    tipo = input("Seleccione una opción: ").strip()
    if tipo == "0":
        return None

    try:
        if tipo == "1":
            nombre = input("Usuario administrador: ")
            clave = getpass("Contraseña: ")
            usuario = autenticar(nombre, clave)
        elif tipo == "2":
            texto_id = input("ID del empleado: ").strip()
            correo = input("Correo del empleado: ").strip()
            empleado_id = int(texto_id)
            if not 1 <= empleado_id <= 9223372036854775807:
                raise ValueError("Ingresa una ID válida dentro del rango permitido.")
            usuario = autenticar_empleado(empleado_id, correo)
        else:
            print("Opción no válida.")
            input("Presione Enter para continuar...")
            return None
    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        input("------------------------------\nPresione Enter para continuar...\n")
        return None
    if usuario is None:
        print("Usuario o contraseña incorrectos.")
        input("------------------------------\nPresione Enter para continuar...\n")
    else:
        print("Sesión iniciada correctamente.")
        print("------------------------------")
        return usuario


def mostrar_perfil(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para ver el perfil.")
        input("Presione Enter para continuar...")
        return
    print(f"Usuario: {usuario_actual['nombre_usuario']}")
    print(f"Empleado: {usuario_actual['empleado_id']}")
    input("Presione Enter para continuar...")


def consultar_indicador(usuario_actual):
    try:
        datos = obtener_datos()
        fecha, clp = extraer_clp(datos)
        print(f"Actualización: {fecha}")
        print(f"1 USD equivale a {clp:.2f} CLP")
    except requests.exceptions.RequestException:
        print("No se pudo consultar el servicio. Intente nuevamente.")
    except (TypeError, ValueError):
        print("La respuesta de la API no es válida.")
    input("Presione Enter para continuar...")


def mostrar_mis_registros(usuario_actual):
    try:
        registros = mi_registros(usuario_actual)
        if not registros:
            print("No tiene registros de tiempo.")
        else:
            for registro in registros:
                print(registro.mostrar_horas())
    except (PermissionError, ValueError) as error:
        print(error)
    input("Presione Enter para continuar...")


def mostrar_mi_departamento(usuario_actual):
    try:
        departamento = mi_departamento(usuario_actual)
        if departamento is None:
            print("No tiene un departamento vinculado.")
        else:
            print(departamento.mostrar_datos())
    except (PermissionError, ValueError) as error:
        print(error)
    input("Presione Enter para continuar...")


def mostrar_mi_ficha(usuario_actual):
    try:
        empleado = mi_ficha(usuario_actual)
        print(empleado.mostrar_datos())
    except (PermissionError, ValueError) as error:
        print(error)
    input("Presione Enter para continuar...")


def actualizar_datos_propios(usuario_actual):
    nombre = input("Nombre nuevo (0 para regresar): ").strip()
    if nombre == "0":
        return
    correo = input("Correo nuevo (0 para regresar): ").strip()
    if correo == "0":
        return
    try:
        actualizar_mis_datos(usuario_actual, nombre, correo)
        print("Datos actualizados correctamente.")
    except (PermissionError, ValueError) as error:
        print(error)
    input("Presione Enter para continuar...")


def mostrar_todos_los_empleados(usuario_actual):
    try:
        empleados = listar_todos(usuario_actual)
        if not empleados:
            print("No hay empleados registrados.")
        else:
            for empleado in empleados:
                print(empleado.mostrar_datos())
    except PermissionError as error:
        print(error)
    input("Presione Enter para continuar...")


def menu_administrador(sesion):
    from main import menu_principal

    exigir_admin(sesion)
    while True:
        limpiar_consola()
        print("\n------------------------------")
        print("----- MENÚ ADMINISTRADOR -----")
        print("------------------------------")
        print("1. Mi ficha")
        print("2. Mis registros")
        print("3. Consultar API")
        print("4. Administrar empleados")
        print("5. Gestionar sistema")
        print("9. Cerrar sesión")
        print("0. Salir")

        opcion = input("Opción: ").strip()
        if opcion in ("0", "9"):
            return opcion
        if opcion == "1":
            mostrar_mi_ficha(sesion)
        elif opcion == "2":
            mostrar_mis_registros(sesion)
        elif opcion == "3":
            consultar_indicador(sesion)
        elif opcion == "4":
            mostrar_todos_los_empleados(sesion)
        elif opcion == "5":
            menu_principal()
        else:
            print("Opción no válida.")
            input("Presione Enter para continuar...")


def menu_empleado(sesion):
    exigir_sesion(sesion)
    while True:
        limpiar_consola()
        print("\n------------------------------")
        print("------- MENÚ EMPLEADO --------")
        print("------------------------------")
        print("1. Mi ficha")
        print("2. Mis registros")
        print("3. Mi departamento")
        print("4. Actualizar mis datos")
        print("9. Cerrar sesión")
        print("0. Salir")

        opcion = input("Opción: ").strip()
        if opcion in ("0", "9"):
            return opcion
        if opcion == "1":
            mostrar_mi_ficha(sesion)
        elif opcion == "2":
            mostrar_mis_registros(sesion)
        elif opcion == "3":
            mostrar_mi_departamento(sesion)
        elif opcion == "4":
            actualizar_datos_propios(sesion)
        else:
            print("Opción no válida.")
            input("Presione Enter para continuar...")


def menu_privado(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"
    if usuario_actual.get("rol") == "admin":
        return menu_administrador(usuario_actual)
    if usuario_actual.get("rol") == "empleado":
        return menu_empleado(usuario_actual)
    print("Rol no válido.")
    input("Presione Enter para continuar...")
    return "9"
