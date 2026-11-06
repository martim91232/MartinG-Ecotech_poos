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
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registrotiempo_dao import RegistroTiempoDAO
from persistencia.asignacion_proyecto_dao import AsignacionProyectoDAO
from dominio.registrotiempo import RegistroTiempo
from servicios.permisos import exigir_admin, exigir_sesion
from servicios.mi_cuenta import (
    mi_ficha,
    mi_registros,
    mi_departamento,
    actualizar_mis_datos,
)
from servicios.indicadores import consultar_indicador as consultar_indicador_servicio
from servicios.indicadores import obtener_historial
from servicios.gestion_empleado import listar_todos
from datetime import datetime
import sqlite3


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
            correo = input("Correo del empleado: ").strip()
            clave = getpass("Contraseña: ")
            usuario = autenticar_empleado(correo, clave)
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
        input("Presione Enter para continuar...")
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
        indicador, origen = consultar_indicador_servicio(usuario_actual)
        print(f"Fecha: {indicador.fecha}")
        print(f"1 USD equivale a {indicador.valor:.2f} {indicador.unidad.split('/')[-1]}")
        print(f"Origen: {origen}")
    except (PermissionError, ValueError) as error:
        print(error)
    input("Presione Enter para continuar...")


def mostrar_historial_indicadores(usuario_actual):
    try:
        historial = obtener_historial(usuario_actual)
        if not historial:
            print("No hay indicadores guardados.")
        else:
            for indicador in historial:
                print(
                    f"{indicador.fecha}: {indicador.valor:.2f} "
                    f"{indicador.unidad} (fuente: {indicador.fuente})"
                )
    except (PermissionError, ValueError) as error:
        print(error)
    input("Presione Enter para continuar...")


def menu_indicadores(usuario_actual):
    exigir_sesion(usuario_actual)
    while True:
        limpiar_consola()
        print("\n------------------------------")
        print("------ MENÚ DE INDICADORES ---")
        print("------------------------------")
        print("1. Consultar valor actualizado")
        print("2. Ver historial guardado")
        print("0. Volver al menú principal")

        opcion = input("Opción: ").strip()
        if opcion == "0":
            return
        if opcion == "1":
            consultar_indicador(usuario_actual)
        elif opcion == "2":
            mostrar_historial_indicadores(usuario_actual)
        else:
            print("Opción no válida.")
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


def _pedir_id(mensaje):
    texto = input(f"{mensaje} (0 para regresar): ").strip()
    if texto == "0":
        return None
    try:
        valor = int(texto)
    except ValueError as error:
        raise ValueError("La ID debe ser un número entero.") from error
    if not 1 <= valor <= 9223372036854775807:
        raise ValueError("La ID está fuera del rango permitido.")
    return valor


def asignar_gerente():
    departamentos = DepartamentoDAO.listar()
    empleados = EmpleadoDAO.listar()
    if not departamentos or not empleados:
        raise ValueError("Se necesita al menos un departamento y un empleado.")
    for departamento in departamentos:
        print(departamento.mostrar_datos())
    id_departamento = _pedir_id("ID del departamento")
    if id_departamento is None:
        return
    departamento = DepartamentoDAO.buscar_por_id(id_departamento)
    if departamento is None:
        raise ValueError("No existe ese departamento.")
    for empleado in empleados:
        print(empleado.mostrar_datos())
    id_empleado = _pedir_id("ID del gerente")
    if id_empleado is None:
        return
    gerente = EmpleadoDAO.buscar_por_id(id_empleado)
    if gerente is None:
        raise ValueError("No existe ese empleado.")
    if not DepartamentoDAO.asignar_gerente(id_departamento, gerente.nombre):
        raise ValueError("No se pudo asignar el gerente.")
    print(f"Gerente asignado: {gerente.nombre}")
    input("Presione Enter para continuar...")


def crear_cuenta_empleado():
    solicitar_registro()


def asignar_empleado_proyecto():
    empleados = EmpleadoDAO.listar()
    proyectos = ProyectoDAO.listar()
    if not empleados or not proyectos:
        raise ValueError("Se necesita al menos un empleado y un proyecto.")
    print("Empleados:")
    for empleado in empleados:
        print(empleado.mostrar_datos())
    id_empleado = _pedir_id("ID del empleado")
    if id_empleado is None:
        return
    if EmpleadoDAO.buscar_por_id(id_empleado) is None:
        raise ValueError("No existe ese empleado.")
    print("Proyectos:")
    for proyecto in proyectos:
        print(proyecto.mostrar_datos())
    id_proyecto = _pedir_id("ID del proyecto")
    if id_proyecto is None:
        return
    if ProyectoDAO.buscar_por_id(id_proyecto) is None:
        raise ValueError("No existe ese proyecto.")
    if AsignacionProyectoDAO.esta_asignado(id_empleado, id_proyecto):
        raise ValueError("El empleado ya está asignado a ese proyecto.")
    AsignacionProyectoDAO.asignar(id_empleado, id_proyecto)
    print("Empleado asignado correctamente.")
    input("Presione Enter para continuar...")


def mostrar_mis_proyectos(sesion):
    exigir_sesion(sesion)
    filas = AsignacionProyectoDAO.proyectos_de_empleado(sesion["empleado_id"])
    if not filas:
        print("No tiene proyectos asignados.")
    else:
        for fila in filas:
            print(ProyectoDAO._fila_a_proyecto(fila).mostrar_datos())
    input("Presione Enter para continuar...")


def registrar_mi_tiempo(sesion):
    exigir_sesion(sesion)
    filas = AsignacionProyectoDAO.proyectos_de_empleado(sesion["empleado_id"])
    if not filas:
        raise ValueError("No tiene proyectos asignados para registrar horas.")
    for fila in filas:
        print(ProyectoDAO._fila_a_proyecto(fila).mostrar_datos())
    id_proyecto = _pedir_id("ID del proyecto")
    if id_proyecto is None:
        return
    if not AsignacionProyectoDAO.esta_asignado(sesion["empleado_id"], id_proyecto):
        raise PermissionError("Solo puede registrar horas en proyectos asignados.")
    fecha = input("Fecha (AAAA-MM-DD, 0 para regresar): ").strip()
    if fecha == "0":
        return
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        horas = float(input("Horas trabajadas: ").strip().replace(",", "."))
    except (TypeError, ValueError) as error:
        raise ValueError("La fecha o las horas no son válidas.") from error
    if not 0 < horas <= 24:
        raise ValueError("Las horas deben ser mayores que 0 y no superar 24.")
    descripcion = input("Descripción (opcional): ").strip()
    RegistroTiempoDAO.insertar(
        RegistroTiempo(
            id_empleado=sesion["empleado_id"],
            id_proyecto=id_proyecto,
            fecha=fecha,
            horas=horas,
            descripcion=descripcion,
        )
    )
    print("Horas registradas correctamente.")
    input("Presione Enter para continuar...")


def ejecutar_accion(funcion, *args):
    try:
        funcion(*args)
    except (PermissionError, ValueError, sqlite3.Error) as error:
        print(error)
        input("Presione Enter para continuar...")


def menu_administrador(sesion):
    from main import menu_principal
    from presentacion.menu_empleado import menu_empleados

    exigir_admin(sesion)
    while True:
        limpiar_consola()
        print("\n------------------------------")
        print("----- MENÚ ADMINISTRADOR -----")
        print("------------------------------")
        print("1. Mi ficha")
        print("2. Mis registros")
        print("3. Menú de indicadores")
        print("4. Administrar empleados")
        print("5. Crear cuenta de empleado")
        print("6. Asignar empleado a proyecto")
        print("7. Asignar gerente de departamento")
        print("8. Gestionar sistema")
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
            menu_indicadores(sesion)
        elif opcion == "4":
            menu_empleados()
        elif opcion == "5":
            ejecutar_accion(crear_cuenta_empleado)
        elif opcion == "6":
            ejecutar_accion(asignar_empleado_proyecto)
        elif opcion == "7":
            ejecutar_accion(asignar_gerente)
        elif opcion == "8":
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
        print("5. Menú de indicadores")
        print("6. Mis proyectos asignados")
        print("7. Registrar horas")
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
        elif opcion == "5":
            menu_indicadores(sesion)
        elif opcion == "6":
            ejecutar_accion(mostrar_mis_proyectos, sesion)
        elif opcion == "7":
            ejecutar_accion(registrar_mi_tiempo, sesion)
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
