
class Item():
    def __init__(self, nombre, tipo, descripcion):
        self.nombre = nombre
        self.tipo = tipo
        self.descripcion = descripcion


class Consumibles(Item):
    def __init__(self, nombre, tipo, descripcion, energia, fuerza, suerte, felicidad):
        super().__init__(nombre, tipo, descripcion)
        self.energia = int(energia)
        self.fuerza = int(fuerza)
        self.suerte = int(suerte)
        self.felicidad = int(felicidad)


class Tesoros(Item):
    def __init__(self, nombre, tipo, descripcion, calidad, cambio):
        super().__init__(nombre, tipo, descripcion)
        self.calidad = int(calidad)
        self.cambio = cambio
