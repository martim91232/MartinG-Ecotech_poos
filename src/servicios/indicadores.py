import math
from email.utils import parsedate_to_datetime

import requests
from persistencia.indicador_dao import IndicadorDAO
from servicios.deserializador_indicador import DeserializadorIndicador
from servicios.permisos import exigir_sesion


def obtener_datos():
    respuesta = requests.get(
        "https://open.er-api.com/v6/latest/USD",
        timeout=(3, 5),
    )
    respuesta.raise_for_status()
    return respuesta.json()


def extraer_clp(datos, moneda="CLP"):
    if not isinstance(datos, dict) or datos.get("result") != "success":
        raise ValueError("La respuesta no contiene un indicador válido.")

    tasas = datos.get("rates")
    valor = tasas.get(moneda) if isinstance(tasas, dict) else None
    if (
        type(valor) not in (int, float)
        or not math.isfinite(valor)
        or valor <= 0
    ):
        raise ValueError("La moneda solicitada no tiene un valor válido.")

    fecha = datos.get("time_last_update_utc")
    if not isinstance(fecha, str):
        raise ValueError("La API no entregó una fecha válida.")
    try:
        fecha_normalizada = parsedate_to_datetime(fecha).date().isoformat()
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError("La API no entregó una fecha válida.") from error
    return fecha_normalizada, valor


def consultar_indicador(sesion):
    exigir_sesion(sesion)
    try:
        indicador = DeserializadorIndicador.desde_api(obtener_datos())
        IndicadorDAO.guardar(indicador)
        return indicador, "API"
    except (requests.exceptions.RequestException, TypeError, ValueError):
        historial = obtener_historial(sesion)
        if historial:
            return historial[0], "BD local"
        raise ValueError("No hay datos disponibles de la API ni respaldo local.")


def obtener_historial(sesion):
    exigir_sesion(sesion)
    return IndicadorDAO.listar()


