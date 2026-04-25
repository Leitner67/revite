
class Cliente:
    def __init__(self, cedula, nombres, apellidos, foto, celular, contraseña, silla_de_ruedas):
        self.__cedula = cedula
        self.__nombres = nombres
        self.__apellidos = apellidos
        self.__foto = foto
        self.__celular = celular
        self.__contraseña = contraseña
        self.__silla_de_ruedas = silla_de_ruedas

    def get_cedula(self):
        return self.__cedula
    
    def get_nombres(self):
        return self.__nombres
    
    def get_apellidos(self):
        return self.__apellidos
    
    def get_foto(self):
        return self.__foto
    
    def get_celular(self):
        return self.__celular

    def get_contraseña(self):
        return self.__contraseña
    
    def get_silla_de_ruedas(self):
        return self.__silla_de_ruedas

    def set_cedula(self, cedula):
        self.__cedula = cedula
    
    def set_nombres(self, nombres):
        self.__nombres = nombres
    
    def set_apellidos(self, apellidos):
        self.__apellidos = apellidos
    
    def set_foto(self, foto):
        self.__foto = foto

    def set_celular(self, celular):
        self.__celular = celular
    
    def set_contraseña(self, contraseña):
        self.__contraseña = contraseña
    
    def set_silla_de_ruedas(self, silla_de_ruedas):
        self.__silla_de_ruedas = silla_de_ruedas

    def __str__(self):
        return f"Cliente: {self.__nombres} {self.__apellidos} (CC: {self.__cedula}, Celular: {self.__celular}, Contraseña: {self.__contraseña})"

