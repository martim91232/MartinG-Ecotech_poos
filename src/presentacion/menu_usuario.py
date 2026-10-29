import getpass
from entradas import pedir_dato
from servicios.autenticacion import registrar_usuario
from servicios.autenticacion import autenticar
from dominio.usuario import Usuario
from getpass import getpass
def solicitar_registro():
    print("=== Registro de Usuario ===")
    try:
        empleado_id=pedir_dato("ID del empleado: ", int)
        nombre_usuario=pedir_dato("Nombre de usuario: ", Usuario.normalizar_usuario)
        clave=pedir_dato("Contraseña: ", Usuario.validar_clave, leer=getpass.getpass)

        if clave != getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden. Vuelva al registro")
            return None
        
        usuario_id=registrar_usuario(empleado_id, nombre_usuario, clave)
    except(TypeError, ValueError) as error:
        print(error)
        return None
    
    print(f"Usuario registrado con éxito. ID de usuario: {usuario_id}")
    return usuario_id

from getpass import getpass
def solicitar_login():
    nombre=input("Usuario: ")
    clave=getpass("contraseña: ")
    try:
        usuario= autenticar(nombre, clave)
    except(TypeError, ValueError) as error: 
            print(error)
            return None
    if usuario is None:
        print("Usuario o contraseña incorrectos.")
    else:
        print(f"Bienvenido, {usuario['nombre_usuario']}.")
    return usuario

def mostrar_perfil(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesion para ver su perfil.")
        return
    print(f"Usuario: {usuario_actual['nombre_usuario']}")
    print(f"Empleado: {usuario_actual['empleado_id']}")

def consultar_indicador(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para consultar indicadores.")
        return
    
    #mostrar_indicadores(usuario_actual)



def menu_privado(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión para acceder al menú privado.")
        return "9"
    while True:
        print("\n=== Menú Privado ===")
        print("1.Registrar usuario","2.Perfil de usuario","3.Consultar indicadores","9.Salir")
        opcion=input("Opción: ").strip

        if opcion in ("0","9"):
            return opcion
        if opcion=="1":
            solicitar_registro()
        elif opcion=="2":
            mostrar_perfil(usuario_actual)
        elif opcion=="3":
            consultar_indicador(usuario_actual)
        else:
            print("Opción inválida. Intente nuevamente.")



