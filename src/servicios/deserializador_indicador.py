
from email.utils import parsedate_to_datetime

from dominio.indicador import Indicador


class DeserializadorIndicador:
    @staticmethod
    def desde_api(datos):
        if not isinstance(datos, dict) or datos.get("result") != "success":
            raise ValueError("La respuesta de la API no es válida.")
        tasas = datos.get("rates")
        valor = tasas.get("CLP") if isinstance(tasas, dict) else None
        fecha = datos.get("time_last_update_utc")
        if not isinstance(fecha, str):
            raise ValueError("La API no entregó una fecha válida.")
        try:
            fecha = parsedate_to_datetime(fecha).date().isoformat()
        except (TypeError, ValueError, OverflowError) as error:
            raise ValueError("La API no entregó una fecha válida.") from error
        return Indicador(fecha, valor)
