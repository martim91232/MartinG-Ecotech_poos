
import math
from email.utils import parsedate_to_datetime

from dominio.indicador import Indicador


class DeserializadorIndicador:
    @staticmethod
    def extraer_clp(datos, moneda="CLP"):
        if not isinstance(moneda, str) or not moneda.strip():
            raise ValueError("La moneda solicitada no es válida.")
        if not isinstance(datos, dict):
            raise ValueError("La respuesta de la API no es válida.")
        if datos.get("result") != "success":
            raise ValueError("La API no devolvió una respuesta exitosa.")

        tasas = datos.get("rates")
        if not isinstance(tasas, dict):
            raise ValueError("La API no entregó tasas de cambio válidas.")

        valor = tasas.get(moneda)
        if (
            type(valor) not in (int, float)
            or not math.isfinite(valor)
            or valor <= 0
        ):
            raise ValueError(f"Valor del {moneda} inválido.")

        fecha = datos.get("time_last_update_utc")
        if not isinstance(fecha, str) or not fecha.strip():
            raise ValueError("La API no entregó una fecha válida.")
        try:
            fecha = parsedate_to_datetime(fecha).date().isoformat()
        except (TypeError, ValueError, OverflowError) as error:
            raise ValueError("La API no entregó una fecha válida.") from error
        return fecha, valor

    @staticmethod
    def desde_api(datos):
        fecha, valor = DeserializadorIndicador.extraer_clp(datos)
        return Indicador(fecha, valor)
