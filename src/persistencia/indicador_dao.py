SQL_GUARDAR = """
INSERT INTO indicador_api
    (fuente, codigo, fecha, valor, unidad, verificado_en)
VALUES (?, ?, ?, ?, ?, ?)
ON CONFLICT (fuente, codigo, fecha) DO UPDATE SET
    valor = excluded.valor,
    unidad = excluded.unidad,
    verificado_en = excluded.verificado_en

"""

from dominio.indicador import Indicador
from persistencia.conexion import abrir_conexion


class IndicadorDAO:
    @staticmethod
    def guardar(indicador):
        conexion = None
        try:
            conexion = abrir_conexion()
            conexion.execute(SQL_GUARDAR, (
                indicador.fuente,
                indicador.codigo,
                indicador.fecha,
                indicador.valor,
                indicador.unidad,
                indicador.verificado_en,
            ))
            conexion.commit()
        except Exception:
            if conexion is not None:
                conexion.rollback()
            raise
        finally:
            if conexion is not None:
                conexion.close()

    @staticmethod
    def listar():
        conexion = None
        try:
            conexion = abrir_conexion()
            filas = conexion.execute(
                "SELECT fuente, fecha, valor, verificado_en "
                "FROM indicador_api ORDER BY fecha DESC"
            ).fetchall()
            return [
                Indicador(
                    fecha=fila[1],
                    valor=fila[2],
                    verificado_en=fila[3],
                    fuente=fila[0],
                )
                for fila in filas
            ]
        finally:
            if conexion is not None:
                conexion.close()
