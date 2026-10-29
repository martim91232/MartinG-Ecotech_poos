class usuario:
    MIN_USUARIO=3
    MAX_USUARIO=40
    MIN_CLAVE=6

    def __ini__(self, nombre_usuario, password_hash, empleado_id, id=None):
        if type(empleado_id) is not int or empleado_id<=0:
            raise TypeError("El ID del empleado debe ser un entero positivo.")
        self.empleado_id=empleado_id
        self.id=id
        self.nombre_usuario=self.normalizar_usuario(nombre_usuario)
        self.password_hash=self.validar_clave(password_hash)

        @classmethod
        def normalizar_usuario(cls,nombre):
            if not isinstance(nombre.strip(), str):
                raise TypeError("El nombre de usuario debe ser una cadena de texto.")
            nombre=nombre.strip().lower()
            if not cls.MIN_USUARIO<=len(nombre)<=cls.MAX_USUARIO:
                raise ValueError(f"El nombre de usuario debe tener entre {cls.MIN_USUARIO} y {cls.MAX_USUARIO} caracteres.")
            if not all(c.isascii() and (c.isalnum() or c =="_"
                                        ) for c in nombre):
                raise ValueError("El nombre de usuario solo puede contener caracteres alfanuméricos y guiones bajos.")
            return nombre
        
        @classmethod
        def validar_clave(cls,clave):
            if not isinstance(clave,str):
                if not isinstance(clave, str):
                    raise TypeError("La clave debe ser una cadena de texto.")
                if len(clave)<cls.MIN_CLAVE:
                    raise ValueError(f"La clave debe tener al menos {cls.MIN_CLAVE} caracteres.")
                return clave




