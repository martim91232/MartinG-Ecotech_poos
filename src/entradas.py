import os
def limpiar_consola():
    os.system("cls" if os.name == "nt" else "clear")


def pedir_dato(mensaje, validador, leer=input):
    while True:
        try:
            return validador(leer(mensaje))
        except (TypeError, ValueError):
            print("Ingresa un valor válido. Intenta nuevamente.")