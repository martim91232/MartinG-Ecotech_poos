import re

from dominio.registrotiempo import RegistroTiempo


class Empleado:
    MAX_NOMBRE = 100
    MAX_CORREO = 150

    @staticmethod
    def validar_nombre(nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if len(nombre.strip()) > Empleado.MAX_NOMBRE:
            raise ValueError(
                f"El nombre no puede superar los {Empleado.MAX_NOMBRE} caracteres."
            )
        if not all(caracter.isalpha() or caracter == " "
                   for caracter in nombre):
            raise ValueError("El nombre solo puede contener letras y espacios.")
        return nombre.strip()

    @staticmethod
    def validar_correo(correo):
        if not isinstance(correo, str) or not correo.strip():
            raise ValueError("El correo no puede estar vacío.")
        correo = correo.strip()
        if len(correo) > Empleado.MAX_CORREO:
            raise ValueError(
                f"El correo no puede superar los {Empleado.MAX_CORREO} caracteres."
            )
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
            raise ValueError("Ingresa un correo válido.")
        return correo

    def __init__(self, nombre: str, correo: str, id=None, id_departamento=None):
        self._id = id
        self._nombre = nombre
        self._correo = correo
        self._id_departamento = id_departamento
        self._horas_registradas: list[RegistroTiempo] = []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        self._correo = valor

    @property
    def id_departamento(self):
        return self._id_departamento

    @id_departamento.setter
    def id_departamento(self, valor):
        self._id_departamento = valor

    @property
    def horas_registradas(self) -> tuple:
        return tuple(self._horas_registradas)

    def mostrar_datos(self) -> str:
        return f"ID: {self.id} - {self.nombre} - {self.correo}"

    def registrar_tiempo(self, tiempo: RegistroTiempo) -> bool:
        self._horas_registradas.append(tiempo)
        return True