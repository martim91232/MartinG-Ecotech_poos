SQL_GUARDAR_SQLITE = """
INSERT INTO indicador_api
    (fuente, codigo, fecha, valor, unidad, verificado_en)
VALUES (?, ?, ?, ?, ?, ?)
ON CONFLICT (fuente, codigo, fecha) DO UPDATE SET
    valor = excluded.valor,
    unidad = excluded.unidad,
    verificado_en = excluded.verificado_en

"""

SQL_GUARDAR_MYSQL = """
INSERT INTO indicador_api
    (fuente, codigo, fecha, valor, unidad, verificado_en)
VALUES (%s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    valor = VALUES(valor),
    unidad = VALUES(unidad),
    verificado_en = VALUES(verificado_en)
"""

from dominio.indicador import Indicador
from persistencia.conexion import abrir_conexion, obtener_motor


class IndicadorDAO:
    @staticmethod
    def guardar(indicador):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            sql = (
                SQL_GUARDAR_SQLITE
                if obtener_motor() == "sqlite"
                else SQL_GUARDAR_MYSQL
            )
            cursor.execute(sql, (
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
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT fuente, fecha, valor, verificado_en "
                "FROM indicador_api ORDER BY fecha DESC"
            )
            filas = cursor.fetchall()
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
