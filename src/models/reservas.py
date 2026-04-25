class Reserva:
    def __init__(self, origen="", destino="", horario="", cliente=None):
        self.__origen = origen
        self.__destino = destino
        self.__horario = horario
        self.__cliente = cliente
    
    def get_origen(self):
        return self.__origen
    
    def get_destino(self):
        return self.__destino
    
    def get_horario(self):
        return self.__horario
    
    def get_cliente(self):
        return self.__cliente
    
    def set_origen(self, origen):
        self.__origen = origen
    
    def set_destino(self, destino):
        self.__destino = destino
    
    def set_horario(self, horario):
        self.__horario = horario
    
    def set_cliente(self, cliente):
        self.__cliente = cliente
    
    def __str__(self):
        cliente_nombre = self.__cliente.get_nombres() if self.__cliente else "Sin asignar"
        return f"Reserva: {self.__origen} -> {self.__destino} ({self.__horario}) - Cliente: {cliente_nombre}"
