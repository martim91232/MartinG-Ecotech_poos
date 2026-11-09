from dominio.registrotiempo import RegistroTiempo


class Empleado:
    MIN_NOMBRE = 2
    MAX_NOMBRE = 100
    MIN_CORREO = 6
    MAX_CORREO = 254

    @classmethod
    def validar_nombre(cls, nombre):
        if not isinstance(nombre, str):
            raise TypeError("El nombre debe ser texto.")
        nombre = nombre.strip()
        if not cls.MIN_NOMBRE <= len(nombre) <= cls.MAX_NOMBRE:
            raise ValueError(
                f"El nombre debe tener entre {cls.MIN_NOMBRE} y "
                f"{cls.MAX_NOMBRE} caracteres."
            )
        if not all(caracter.isalpha() or caracter == " "
                for caracter in nombre):
            raise ValueError("El nombre solo puede contener letras y espacios.")
        return nombre

    @classmethod
    def validar_correo(cls, correo):
        if not isinstance(correo, str):
            raise TypeError("El correo debe ser texto.")
        correo = correo.strip()
        if not cls.MIN_CORREO <= len(correo) <= cls.MAX_CORREO:
            raise ValueError("Correo fuera del largo permitido.")
        if any(caracter.isspace() for caracter in correo):
            raise ValueError("El correo no debe contener espacios.")
        if correo.count("@") != 1:
            raise ValueError("El correo debe contener un solo @.")
        usuario, dominio = correo.split("@")
        if not usuario or "." not in dominio:
            raise ValueError("Use un correo como nombre@empresa.cl.")
        if any(not parte for parte in dominio.split(".")):
            raise ValueError("El dominio contiene puntos inválidos.")
        return correo

    def __init__(self, nombre: str, correo: str, id=None, id_departamento=None):
        self._id = id
        self._nombre = self.validar_nombre(nombre)
        self._correo = self.validar_correo(correo)
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
        self._nombre = self.validar_nombre(valor)

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        self._correo = self.validar_correo(valor)

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