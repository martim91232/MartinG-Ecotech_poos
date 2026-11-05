from servicios.permisos import exigir_sesion
from persistencia.registrotiempo_dao import RegistroTiempoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.departamento_dao import DepartamentoDAO
from dominio.empleado import Empleado

def mi_registros(sesion):
    exigir_sesion(sesion)
    return RegistroTiempoDAO.listar_por_empleado(
        sesion["empleado_id"]
    )

def mi_ficha(sesion):
    exigir_sesion(sesion)
    empleado = EmpleadoDAO.buscar_por_id(sesion["empleado_id"])
    if empleado is None:
        raise ValueError("No se encontró el empleado.")
    return empleado

def mi_departamento(sesion):
    empleado = mi_ficha(sesion)
    if empleado.id_departamento is None:
        return None
    return DepartamentoDAO.buscar_por_id(empleado.id_departamento)

def actualizar_mis_datos(sesion, nombre, correo):
    exigir_sesion(sesion)
    nombre = Empleado.validar_nombre(nombre)
    correo = Empleado.validar_correo(correo)
    empleado = EmpleadoDAO.buscar_por_id(sesion["empleado_id"])
    if empleado is None:
        raise ValueError("No se encontró el empleado.")

    empleado.nombre = nombre
    empleado.correo = correo
    if not EmpleadoDAO.actualizar(empleado):
        raise ValueError("No se pudieron actualizar los datos.")
    return empleado

