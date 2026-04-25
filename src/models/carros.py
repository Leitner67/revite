class Carro:
    def __init__(self, marca, modelo, ano, placa):
        self.__marca = marca
        self.__modelo = modelo
        self.__ano = ano
        self.__placa = placa

    def get_marca(self):
        return self.__marca
    def get_modelo(self):
        return self.__modelo
    def get_ano(self):
        return self.__ano
    def get_placa(self):
        return self.__placa
    
    def set_marca(self, marca):
        self.__marca = marca
    def set_modelo(self, modelo):
        self.__modelo = modelo
    def set_ano(self, ano):
        self.__ano = ano
    def set_placa(self, placa):
        self.__placa = placa

    def __str__(self):
        return f"{self.__marca} {self.__modelo} ({self.__ano}) - Placa: {self.__placa}"
    
