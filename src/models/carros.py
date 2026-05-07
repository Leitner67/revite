class Carro:
    def __init__(self, marca, modelo, ano, placa):
        self._marca = marca
        self._modelo = modelo
        self._ano = ano
        self._placa = placa

    def _validar_texto(self, value, mensaje_error):
        if not value or not isinstance(value, str):
            raise ValueError(mensaje_error)
        return value.strip()

    def get_marca(self):
        return self._marca

    def get_modelo(self):
        return self._modelo

    def get_ano(self):
        return self._ano

    def get_placa(self):
        return self._placa

    def set_marca(self, marca):
        self._marca = self._validar_texto(marca, "La marca debe ser un texto válido")

    def set_modelo(self, modelo):
        self._modelo = self._validar_texto(modelo, "El modelo debe ser un texto válido")

    def set_ano(self, ano):
        try:
            ano_int = int(ano)
            if ano_int < 1900 or ano_int > 2030:
                raise ValueError("El año debe estar entre 1900 y 2030")
            self._ano = ano_int
        except (ValueError, TypeError):
            raise ValueError("El año debe ser un número válido")

    def set_placa(self, placa):
        self._placa = self._validar_texto(placa, "La placa debe ser un texto válido").upper()

    def descripcion_corta(self):
        return f"{self._marca} {self._modelo} - {self._placa}"

    def to_dict(self):
        return {
            'marca': self._marca,
            'modelo': self._modelo,
            'ano': self._ano,
            'placa': self._placa
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            marca=data.get('marca', ''),
            modelo=data.get('modelo', ''),
            ano=data.get('ano', 0),
            placa=data.get('placa', '')
        )
    
    def __str__(self):
        return f"{self._marca} {self._modelo} ({self._ano}) - Placa: {self._placa}"
    
