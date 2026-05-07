class Cliente:
    def __init__(self, cedula, nombres, apellidos, foto, celular, contraseña):
        self._cedula = cedula
        self._nombres = nombres
        self._apellidos = apellidos
        self._foto = foto
        self._celular = celular
        self._contraseña = contraseña

    def _validar_texto(self, value, mensaje_error):
        if not value or not isinstance(value, str):
            raise ValueError(mensaje_error)
        return value.strip()

    def get_cedula(self):
        return self._cedula

    def get_nombres(self):
        return self._nombres

    def get_apellidos(self):
        return self._apellidos

    def get_foto(self):
        return self._foto

    def get_celular(self):
        return self._celular

    def get_contraseña(self):
        return self._contraseña

    def set_cedula(self, cedula):
        self._cedula = self._validar_texto(cedula, "La cédula debe ser válida")

    def set_nombres(self, nombres):
        self._nombres = self._validar_texto(nombres, "El nombre debe ser válido")

    def set_apellidos(self, apellidos):
        self._apellidos = self._validar_texto(apellidos, "Los apellidos deben ser válidos")

    def set_foto(self, foto):
        self._foto = foto.strip() if foto else ''

    def set_celular(self, celular):
        self._celular = self._validar_texto(celular, "El celular debe ser válido")

    def set_contraseña(self, contraseña):
        self._contraseña = self._validar_texto(contraseña, "La contraseña debe ser válida")

    def nombre_completo(self):
        return f"{self._nombres} {self._apellidos}".strip()

    def to_dict(self):
        return {
            'cedula': self._cedula,
            'nombres': self._nombres,
            'apellidos': self._apellidos,
            'foto': self._foto,
            'celular': self._celular,
            'contraseña': self._contraseña
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            cedula=data.get('cedula', ''),
            nombres=data.get('nombres', ''),
            apellidos=data.get('apellidos', ''),
            foto=data.get('foto', ''),
            celular=data.get('celular', ''),
            contraseña=data.get('contraseña', '')
        )

    def __str__(self):
        return f"Cliente: {self._nombres} {self._apellidos} (CC: {self._cedula}, Celular: {self._celular}, Contraseña: {self._contraseña})"

