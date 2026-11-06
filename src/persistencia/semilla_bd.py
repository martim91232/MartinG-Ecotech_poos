from dominio.departamento import Departamento
from dominio.empleado import Empleado
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from servicios.autenticacion import registrar_usuario
from persistencia.usuario_dao import UsuarioDAO

CLAVE_INICIAL_EMPLEADOS = "Empleado123*"


def cargar_departamentos(mostrar_mensajes=True):
    datos = [
        ("Marketing Digital", "Estrategias de posicionamiento y gestion de redes"),
        ("Soporte Tecnico", "Asistencia al usuario y resolucion de incidencias"),
        ("Logistica", "Control de inventarios y distribucion de productos"),
        ("Calidad y Procesos", "Auditoria de estandares y mejora continua"),
        ("Atencion al Cliente", "Gestion de consultas, reclamos y fidelizacion"),
    ]

    nombres_existentes = {
        departamento.nombre for departamento in DepartamentoDAO.listar()
    }

    for nombre, descripcion in datos:
        if nombre in nombres_existentes:
            if mostrar_mensajes:
                print(f"Ya existe: {nombre}")
            continue

        departamento = Departamento(nombre, descripcion)
        DepartamentoDAO.insertar(departamento)
        nombres_existentes.add(nombre)
        if mostrar_mensajes:
            print(f"Creado: {nombre}")


def cargar_empleados(departamento_demo=None, mostrar_mensajes=True):
    departamentos = DepartamentoDAO.listar()
    if not departamentos:
        raise ValueError(
            "No existe ningún departamento registrado; "
            "cargue los departamentos antes que los empleados."
        )

    datos = [
        ("Alejandro Vargas", "alejandro.vargas@ecotech.cl"),
        ("Fernanda Tapia", "fernanda.tapia@ecotech.cl"),
        ("Sebastián Cáceres", "sebastian.caceres@ecotech.cl"),
        ("Natalia Fuentes", "natalia.fuentes@ecotech.cl"),
        ("Javier Carrasco", "javier.carrasco@ecotech.cl"),
        ("Constanza Poblete", "constanza.poblete@ecotech.cl"),
        ("Matías Donoso", "matias.donoso@ecotech.cl"),
        ("Isidora Vergara", "isidora.vergara@ecotech.cl"),
        ("Nicolás Henríquez", "nicolas.henriquez@ecotech.cl"),
        ("Francisca Lagos", "francisca.lagos@ecotech.cl"),
        ("Gonzalo Ojeda", "gonzalo.ojeda@ecotech.cl"),
        ("Bárbara Orellana", "barbara.orellana@ecotech.cl"),
        ("Rodrigo Farías", "rodrigo.farias@ecotech.cl"),
        ("Javiera Saavedra", "javiera.saavedra@ecotech.cl"),
        ("Felipe Valenzuela", "felipe.valenzuela@ecotech.cl"),
        ("Catalina Sanhueza", "catalina.sanhueza@ecotech.cl"),
        ("Ignacio Aguilera", "ignacio.aguilera@ecotech.cl"),
        ("Ángela Sepúlveda", "angela.sepulveda@ecotech.cl"),
        ("Claudio Maldonado", "claudio.maldonado@ecotech.cl"),
        ("Macarena Baeza", "macarena.baeza@ecotech.cl"),
    ]

    for indice, (nombre, correo) in enumerate(datos):
        departamento = departamentos[indice % len(departamentos)]
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            if existente.id_departamento != departamento.id:
                existente.id_departamento = departamento.id
                EmpleadoDAO.actualizar(existente)
            if mostrar_mensajes:
                print(f"Ya existe: {correo}")
            continue
        empleado = Empleado(
            nombre,
            correo,
            id_departamento=departamento.id
        )
        EmpleadoDAO.insertar(empleado)
        if mostrar_mensajes:
            print(f"Creado: {correo}")

def cargar_usuarios(mostrar_mensajes=True):
    usuarios_existentes = UsuarioDAO.listar()
    admin = next(
        (usuario for usuario in usuarios_existentes
        if usuario.nombre_usuario == "admin"),
        None,
    )
    empleado_admin = EmpleadoDAO.buscar_por_correo(
        "alejandro.vargas@ecotech.cl"
    )

    if admin is None and empleado_admin is not None:
        try:
            usuario_id = registrar_usuario(
                empleado_admin.id, "admin", "Admin123*", rol="admin"
            )
            if mostrar_mensajes:
                print(f"Creado: admin (ID {usuario_id})")
            usuarios_existentes = UsuarioDAO.listar()
        except (TypeError, ValueError):
            if mostrar_mensajes:
                print("No se pudo crear el usuario admin")
    elif mostrar_mensajes and admin is not None:
        print("Ya existe: admin")

    empleados = EmpleadoDAO.listar()
    cuentas_por_empleado = {
        usuario.empleado_id for usuario in usuarios_existentes
    }
    for empleado in empleados:
        if empleado.id in cuentas_por_empleado:
            continue

        nombre_usuario = empleado.correo.split("@", 1)[0].replace(".", "_")
        try:
            usuario_id = registrar_usuario(
                empleado.id,
                nombre_usuario,
                CLAVE_INICIAL_EMPLEADOS,
                rol="empleado",
            )
            cuentas_por_empleado.add(empleado.id)
            if mostrar_mensajes:
                print(
                    f"Creada cuenta de empleado: {empleado.correo} "
                    f"(ID {usuario_id})"
                )
        except (TypeError, ValueError):
            if mostrar_mensajes:
                print(f"No se pudo crear cuenta para: {empleado.correo}")
