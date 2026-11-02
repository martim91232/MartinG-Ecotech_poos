from getpass import getpass
from entradas import pedir_dato, limpiar_consola
from servicios.autenticacion import autenticar, registrar_usuario
from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO


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
    nombre = input("Usuario: ")
    clave = getpass("Contraseña: ")
    try:
        usuario = autenticar(nombre, clave)
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
    if usuario_actual is None:
        print("Inicie sesión para consultar indicadores.")
        return


def menu_privado(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"
    while True:
        limpiar_consola()
        print("\n------------------------------")
        print("1 Registrar, 2 Perfil, 3 Menú principal, 9 Cerrar sesión, 0 Salir")
        opcion = input("Opción: ").strip()
        if opcion in ("0", "9"):
            return opcion
        if opcion == "1":
            solicitar_registro()
        elif opcion == "2":
            mostrar_perfil(usuario_actual)
        elif opcion == "3":
            return "3"
        else:
            print("Opción no válida.")
            input("------------------------------\nPresione Enter para continuar...\n")
