import bcrypt
from dominio.usuario import Usuario
from persistencia.usuario_dao import UsuarioDAO

MAX_BYTES_BCRYPT = 72  # Limite de bytes para bcrypt
def crear_hash(clave):
    clave = Usuario.validar_clave(clave)
    clave_bytes = clave.encode("utf-8")

    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError(f"La clave no puede exceder {MAX_BYTES_BCRYPT} bytes.")

def registrar_usuario(empleado_id, nombre, clave):
    nombre=Usuario.normalizar_usuario(nombre)
    if UsuarioDAO.buscar_por_nombre(nombre) is not None:
        raise ValueError(f"El nombre de usuario '{nombre}' ya está en uso.")
    
    hash_guardado=crear_hash(clave)
    usuario=Usuario(empleado_id, nombre, hash_guardado)
    return UsuarioDAO.insertar(usuario)



def autenticar(nombre, clave):
    nombre=Usuario.normalizar_usuario(nombre)
    if not isinstance(clave, str):
        return None
    datos = clave.encode("utf-8")
    if not 0 <len(datos)<= MAX_BYTES_BCRYPT:
        return None
    cuenta=UsuarioDAO.buscar_por_nombre(nombre)

    if cuenta is None:
        print(f"No se encontró la cuenta para el usuario '{nombre}'.")
        return None
    
    if not bcrypt.checkpw(datos, cuenta.password_hash.encode("utf-8")):
        print(f"Contraseña incorrecta para el usuario '{nombre}'.")
        return None
    return {"id": cuenta.id, "empleado_id": cuenta.empleado_id,
            "nombre_usuario": cuenta.nmbre_usuario}