from datetime import datetime
import math


class Indicador:
    def __init__(self, fecha, valor, verificado_en=None,
                fuente="api_dolar_curso"):
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except (TypeError, ValueError) as error:
            raise ValueError("La fecha del indicador no es válida.") from error
        if type(valor) not in (int, float) or not math.isfinite(valor) or valor <= 0:
            raise ValueError("El valor del indicador debe ser positivo y finito.")
        if not isinstance(fuente, str) or not fuente.strip():
            raise ValueError("La fuente del indicador no puede estar vacía.")

        self.fecha = fecha
        self.valor = float(valor)
        self.fuente = fuente.strip()
        self.codigo = "dolar"
        self.unidad = "CLP/USD"
        self.verificado_en = verificado_en or datetime.utcnow().isoformat()


indicador = Indicador