
from dominio.indicador import Indicador


class DeserializadorIndicador:
    @staticmethod
    def desde_api(datos):
        if not isinstance(datos, dict) or datos.get("result") != "success":
            raise ValueError("La respuesta de la API no es válida.")
        tasas = datos.get("rates")
        valor = tasas.get("CLP") if isinstance(tasas, dict) else None
        fecha = datos.get("time_last_update_utc")
        if not isinstance(fecha, str) or len(fecha) < 10:
            raise ValueError("La API no entregó una fecha válida.")
        return Indicador(fecha[:10], valor)
