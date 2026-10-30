from persistencia.crear_bd import crear_tablas
from presentacion.menu_departamento import menu_departamento
from presentacion.menu_empleado import menu_empleados
from presentacion.menu_proyecto import menu_proyecto
from presentacion.menu_registrotiempo import menu_registro_tiempo
from persistencia.semilla_bd import cargar_departamentos, cargar_empleados, cargar_usuarios
from presentacion.menu_usuario import solicitar_login, solicitar_registro, menu_privado

def menu_principal():
    opcion = ""
    while opcion != "0":
        print("\n-----MENU PRINCIPAL ECOTECH -----")
        print("1. Departamentos")
        print("2. Empleados")
        print("3. Proyectos")
        print("4. Registro de tiempo")
        print("0. Volver al Menú de Usuario")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            menu_departamento()
        elif opcion == "2":
            menu_empleados()
        elif opcion == "3":
            menu_proyecto()
        elif opcion == "4":
            menu_registro_tiempo()
        elif opcion == "0":
            print("Volviendo...")
        else:
            print("Opción no válida.")
            input("Presione Enter para continuar...")

def main():
    usuario_actual = None
    while True:
        if usuario_actual is None:
            print("\n-----MENU DE USUARIO ECOTECH -----")
            print("1. Iniciar sesión")
            print("2. Registrar usuario")
            print("0. Salir")

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                usuario_actual = solicitar_login()
            elif opcion == "2":
                solicitar_registro()
            elif opcion == "0":
                print("Hasta luego.")
                break
            else:
                print("Opción no válida.")
        else:
            respuesta = menu_privado(usuario_actual)
            if respuesta == "9":
                usuario_actual = None
            elif respuesta == "0":
                print("Hasta luego.")
                break
            elif respuesta == "3":
                menu_principal()


if __name__ == "__main__":
    crear_tablas()
    cargar_departamentos(mostrar_mensajes=False)
    cargar_empleados(mostrar_mensajes=False)
    cargar_usuarios(mostrar_mensajes=False)

    main()
