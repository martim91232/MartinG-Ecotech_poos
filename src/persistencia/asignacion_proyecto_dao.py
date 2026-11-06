from persistencia.conexion import abrir_conexion, marcador_sql


class AsignacionProyectoDAO:
    @staticmethod
    def asignar(id_empleado, id_proyecto):
        conexion = None
        try:
            conexion = abrir_conexion()
            marca = marcador_sql()
            conexion.execute(
                f"INSERT INTO empleado_proyecto (id_empleado, id_proyecto) "
                f"VALUES ({marca}, {marca})",
                (id_empleado, id_proyecto),
            )
            conexion.commit()
        except Exception:
            if conexion is not None:
                conexion.rollback()
            raise
        finally:
            if conexion is not None:
                conexion.close()

    @staticmethod
    def quitar(id_empleado, id_proyecto):
        conexion = None
        try:
            conexion = abrir_conexion()
            marca = marcador_sql()
            cursor = conexion.execute(
                f"DELETE FROM empleado_proyecto "
                f"WHERE id_empleado = {marca} AND id_proyecto = {marca}",
                (id_empleado, id_proyecto),
            )
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            if conexion is not None:
                conexion.rollback()
            raise
        finally:
            if conexion is not None:
                conexion.close()

    @staticmethod
    def esta_asignado(id_empleado, id_proyecto):
        conexion = None
        try:
            conexion = abrir_conexion()
            marca = marcador_sql()
            fila = conexion.execute(
                f"SELECT 1 FROM empleado_proyecto "
                f"WHERE id_empleado = {marca} AND id_proyecto = {marca}",
                (id_empleado, id_proyecto),
            ).fetchone()
            return fila is not None
        finally:
            if conexion is not None:
                conexion.close()

    @staticmethod
    def proyectos_de_empleado(id_empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            marca = marcador_sql()
            return conexion.execute(
                f"""
                SELECT p.id, p.nombre, p.descripcion, p.fecha_inicio,
                    p.fecha_fin, p.estado
                FROM proyecto p
                JOIN empleado_proyecto ep ON ep.id_proyecto = p.id
                WHERE ep.id_empleado = {marca}
                ORDER BY p.id
                """,
                (id_empleado,),
            ).fetchall()
        finally:
            if conexion is not None:
                conexion.close()
