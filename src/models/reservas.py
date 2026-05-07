class Reserva:
    def __init__(self, origen, destino, horario, cliente):
        self._origen = origen
        self._destino = destino
        self._horario = horario
        self._cliente = cliente

    def _validar_texto(self, value, mensaje_error):
        if not isinstance(value, str):
            raise ValueError(mensaje_error)
        return value.strip()

    def get_origen(self):
        return self._origen

    def get_destino(self):
        return self._destino

    def get_horario(self):
        return self._horario

    def get_cliente(self):
        return self._cliente

    def set_origen(self, origen):
        self._origen = self._validar_texto(origen, "El origen debe ser un texto válido")

    def set_destino(self, destino):
        self._destino = self._validar_texto(destino, "El destino debe ser un texto válido")

    def set_horario(self, horario):
        self._horario = self._validar_texto(horario, "El horario debe ser un texto válido")

    def set_cliente(self, cliente):
        self._cliente = cliente

    def resumen_ruta(self):
        return f"{self._origen} -> {self._destino} ({self._horario})"

    def to_dict(self, include_cliente=True):
        data = {
            'origen': self._origen,
            'destino': self._destino,
            'horario': self._horario
        }
        if include_cliente and self._cliente:
            data['cedula_cliente'] = self._cliente.get_cedula()
        return data
    
    @classmethod
    def from_dict(cls, data, cliente):
        return cls(
            origen=data.get('origen', ''),
            destino=data.get('destino', ''),
            horario=data.get('horario', ''),
            cliente=cliente
        )
    
    def __str__(self):
        cliente_nombre = self._cliente.get_nombres() if self._cliente else "Sin asignar"
        return f"Reserva: {self._origen} -> {self._destino} ({self._horario}) - Cliente: {cliente_nombre}"
