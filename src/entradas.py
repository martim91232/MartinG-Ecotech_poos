import os
def limpiar_consola():
    os.system("cls" if os.name == "nt" else "clear")


def pedir_dato(mensaje, validador, leer=input, permitir_regreso=False):
    while True:
        try:
            entrada = leer(mensaje)
            if permitir_regreso and entrada.strip() == "0":
                return None
            return validador(entrada)
        except (TypeError, ValueError) as error:
            print(f"{error} Intenta nuevamente.")