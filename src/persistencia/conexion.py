import os
import sqlite3
from pathlib import Path
import pymysql
from dotenv import load_dotenv

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
load_dotenv(RAIZ_PROYECTO / ".env")
load_dotenv(RAIZ_PROYECTO / "src" / ".env", override=False)


def obtener_motor():
    return os.getenv("DB_ENGINE", "sqlite").lower()


def marcador_sql():
    if obtener_motor() == "sqlite":
        return "?"
    return "%s"


def abrir_conexion():
    motor = obtener_motor()
    if motor == "sqlite":
        nombre_bd = os.getenv("DB_NAME", "ecotech.db")
        ruta_bd = Path(nombre_bd)
        if not ruta_bd.is_absolute():
            ruta_bd = RAIZ_PROYECTO / ruta_bd
        ruta_bd.parent.mkdir(parents=True, exist_ok=True)
        conexion = sqlite3.connect(str(ruta_bd))
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion

    if motor == "mysql":
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
        )

    raise ValueError(f"Motor no soportado: {motor}")
