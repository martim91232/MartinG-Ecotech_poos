import math

import requests


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

    return datos.get("time_last_update_utc"), valor

