from clases_items import Consumibles, Tesoros
import parametros
from random import randint
import manejo_archivos


class Arena:
    def __init__(self, nombre, tipo, rareza, humedad, dureza, estatica):
        self.nombre = nombre
        self.tipo = tipo
        self.rareza = int(rareza)
        self.humedad = int(humedad)
        self.dureza = int(dureza)
        self.estatica = int(estatica)
        self.items = []    # lista de items
        self.dificultad = round((self.rareza + self.humedad + self.dureza + self.estatica) / 40, 2)
        self.__prob_item = parametros.PROB_ENCONTRAR_ITEM
        self.__prob_tesoro = parametros.PROB_ENCONTRAR_TESORO
        self.__prob_consumible = parametros.PROB_ENCONTRAR_CONSUMIBLE

        # instancio los items con su clase respectiva y los meto en self.items
        for entry in manejo_archivos.lista_tesoros:
            self.items.append(Tesoros(entry.name, 'tesoro', entry.descripcion, *entry[2:]))
        for entry in manejo_archivos.lista_consumibles:
            self.items.append(Consumibles(entry.name, 'consumible', *entry[1:]))

    @property
    def prob_item(self):
        return self.__prob_item

    @property
    def prob_tesoro(self):
        return self.__prob_tesoro

    @property
    def prob_consumible(self):
        return self.__prob_consumible


class ArenaMojada(Arena):
    '''
    ocurre cuando llueve sobre una arena normal, prob_consumible = 1 y hay igual probabilidad
    de encontrar un consumible o un tesoro
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__prob_consumible = 0.5
        self.__prob_item = 1
        self.__prob_tesoro = 0.5

    def __str__(self) -> str:
        return 'mojada'


class ArenaNormal(Arena):
    '''
    arena normal, dificultad ponderada por POND_ARENA_NORMAL
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dificultad = self.dificultad * parametros.POND_ARENA_NORMAL

    def __str__(self) -> str:
        return 'normal'


class ArenaRocosa(Arena):
    '''
    se genera cuando ocurre un terremoto sobre una arena normal
    altera la dificultad
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dificultad = round(
            (self.rareza + self.humedad + 2 * self.dureza + self.estatica) / 50, 2)

    def __str__(self) -> str:
        return 'rocosa'


class ArenaMagnetica(ArenaRocosa, ArenaMojada):
    """
    se genera si ocurre un terremoto sobra una arena mojada o si ocurre lluvia sobre una rocosa
    IMPORTANTE = se debe utilizar el metodo cambiar_dia al final de cada dia para que asi
    se cambie self.humedad y self.dureza por un randint(1, 10)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__prob_consumible = 0.5
        self.__prob_item = 1
        self.__prob_tesoro = 0.5
        self.dificultad = round(
            (self.rareza + self.humedad + 2 * self.dureza + self.estatica) / 50, 2)

    def cambiar_atributo_nuevo_dia(self):
        '''
        cambia el valor de humedad y dureza a un entero al azar entre 1 y 10
        '''
        self.humedad = randint(1, 10)
        self.dureza = randint(1, 10)

    def __str__(self) -> str:
        return 'magnetica'
