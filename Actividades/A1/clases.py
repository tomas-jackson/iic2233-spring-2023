from abc import ABC, abstractmethod


class Animal(ABC):
    identificador = 0

    def __init__(self, peso, nombre, *args, **kwargs) -> None:
        self.peso = peso
        self.nombre = nombre
        self.__energia = 100
        self.identificador = Animal.identificador
        Animal.identificador += 1

    @property
    def energia(self):
        return self.__energia

    @energia.setter
    def energia(self, new):
        if new < 0:
            self.__energia = 0
        else:
            self.__energia = new

    @abstractmethod
    def desplazarse(self):
        pass


class Terrestre(Animal):
    def __init__(self, cantidad_patas, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cantidad_patas = cantidad_patas

    def energia_gastada_por_desplazamiento(self):
        return self.peso * 5

    def desplazarse(self):
        self.energia -= self.energia_gastada_por_desplazamiento()
        return 'caminando...'


class Acuatico(Animal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def energia_gastada_por_desplazamiento(self):
        return self.peso * 2

    def desplazarse(self):
        self.energia -= self.energia_gastada_por_desplazamiento()
        return 'nadando...'


class Perro(Terrestre):
    def __init__(self, raza, *args, **kwargs):
        super().__init__(cantidad_patas=4, *args, **kwargs)
        self.raza = raza

    def ladrar(self):
        return 'guau guau'


class Pez(Acuatico):
    def __init__(self, color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color

    def nadar(self):
        return 'moviendo aleta'


class Ornitorrinco(Acuatico, Terrestre):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def desplazarse(self):
        energia = self.energia
        gasto_energetico_agua = Acuatico.energia_gastada_por_desplazamiento(self)
        gasto_energetico_tierra = Terrestre.energia_gastada_por_desplazamiento(self)
        ret = Acuatico.desplazarse(self) + Terrestre.desplazarse(self)
        gasto = round((gasto_energetico_agua + gasto_energetico_tierra) / 2)
        self.energia = energia
        self.energia -= gasto
        return ret


if __name__ == '__main__':

    perro = Perro(nombre='Pongo', raza='Dalmata', peso=3)
    pez = Pez(nombre='Nemo', color='rojo', peso=1)
    ornitorrinco = Ornitorrinco(nombre='Perry el ortitorico', peso=10, cantidad_patas=6)

    perro.desplazarse()
    pez.desplazarse()
    ornitorrinco.desplazarse()
