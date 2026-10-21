# En un archivo Python de prueba:
import requests
def obtener_datos():
    respuesta = requests.get(
    "https://open.er-api.com/v6/latest/USD",
    timeout=(5, 8),)
    respuesta.raise_for_status()
    return respuesta.json()
         

from datetime import datetime
import math
def extraer_clp(datos):
    # Verificar que la respuesta sea un diccionario.
    if not isinstance(datos, dict):
        raise ValueError("Respuesta inesperada.")

    # Obtener el diccionario de tasas de cambio ('rates').
    rates = datos.get("rates")
    if not isinstance(rates, dict) or not rates:
        raise ValueError("No hay tasas de cambio disponibles.")

    # Obtener el valor específico para el CLP.
    valor = rates.get("CLP")

    # Aceptar solo números finitos y mayores que cero.
    if (
        type(valor) not in (int, float)
        or not math.isfinite(valor)
        or valor <= 0
    ):
        raise ValueError("Valor del indicador inválido.")

    # Obtener la fecha desde 'time_last_update_utc' o usar la fecha actual si no existe
    fecha_str = datos.get("time_last_update_utc")
    if fecha_str:
        # Opcional: puedes parsearla o devolver el string tal cual viene en la API
        fecha = fecha_str
    else:
        fecha = datetime.utcnow().strftime("%Y-%m-%d")

    # Devolver la fecha y el valor como una tupla.
    return fecha, valor

# Ejemplo de uso:
# datos = obtener_datos()
# fecha, valor = extraer_clp(datos)
# print(fecha)
# print(valor)

 

               


