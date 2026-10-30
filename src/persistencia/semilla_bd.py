from dominio.departamento import Departamento
from dominio.empleado import Empleado
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from servicios.autenticacion import registrar_usuario
from persistencia.usuario_dao import UsuarioDAO


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
    if isinstance(departamento_demo, Departamento):
        departamento_demo = departamento_demo.id

    if departamento_demo is None:
        departamentos = DepartamentoDAO.listar()
        departamento = next(
            (
                item for item in departamentos
                if item.nombre == "Soporte Tecnico"
            ),
            departamentos
        )
        if departamento is None:
            raise ValueError(
                "No existe ningún departamento registrado; "
                "cargue los departamentos antes que los empleados."
            )
        departamento_demo = departamento.id

    if DepartamentoDAO.buscar_por_id(departamento_demo) is None:
        raise ValueError(
            f"No existe el departamento con ID {departamento_demo}."
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

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            if mostrar_mensajes:
                print(f"Ya existe: {correo}")
            continue
        empleado = Empleado(
            nombre,
            correo,
            id_departamento=departamento_demo
        )
        EmpleadoDAO.insertar(empleado)
        if mostrar_mensajes:
            print(f"Creado: {correo}")

def cargar_usuarios(mostrar_mensajes=True):
    empleado = EmpleadoDAO.buscar_por_correo("alejandro.vargas@ecotech.cl")
    if empleado is None:
        return

    usuarios_existentes = UsuarioDAO.listar()
    if any(u.nombre_usuario == "admin" for u in usuarios_existentes):
        if mostrar_mensajes:
            print("Ya existe: admin")
        return

    try:
        usuario_id = registrar_usuario(empleado.id, "admin", "Admin123*")
        if usuario_id:
            if mostrar_mensajes:
                print("Creado: admin")
    except (TypeError, ValueError):
        if mostrar_mensajes:
            print("No se pudo crear el usuario admin")
