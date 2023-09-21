from clases_arenas import ArenaMojada, ArenaMagnetica
import parametros
from random import choices, choice
from abc import ABC, abstractmethod
from funciones import mantener_entre_extremos, reducir_dia


class Excavador(ABC):      # asumo que todos los excavadores van a tener un tipo especifico
    def __init__(self, arena, nombre, edad, energia, fuerza, suerte, felicidad):
        self.nombre = nombre
        self._edad = int(edad)
        self._energia = int(energia)
        self._fuerza = int(fuerza)
        self._suerte = int(suerte)
        self._felicidad = int(felicidad)
        self._dias_para_descansar = 0

        # aca instancio la arena inicial, posteriormente guardara la arena actual
        self._arena = arena
        if type(self._arena) == ArenaMojada or type(self._arena) == ArenaMagnetica:
            self._prob_item = 1.0
        else:
            self._prob_item = self.arena.prob_item * (self.suerte / 10)

    # bajo esta linea defino properties y sus setters

    @property
    def energia(self):
        '''
        property, mantiene el la energia entre 0 y 100
        '''
        return self._energia

    @energia.setter
    def energia(self, new):
        self._energia = mantener_entre_extremos(0, 100, new)

    # esta propiedad se usa para cambiar los dias que faltan por descansar de un excavador
    # si no le quedan dias, se queda como 0, si cumple el ultimo dia, queda como 0 y ademas
    # la energia se reestablece en 100

    @property
    def dias_para_descansar(self):
        return self._dias_para_descansar

    @dias_para_descansar.setter
    def dias_para_descansar(self, new):
        nuevo_valor = reducir_dia(self._dias_para_descansar, new)
        if type(nuevo_valor) == tuple:
            self._dias_para_descansar = nuevo_valor[0]
            self._energia = nuevo_valor[1]
            print(f' >> {self.nombre} desperto!!!')
        elif nuevo_valor == 0:
            self._dias_para_descansar = nuevo_valor
        else:
            self._dias_para_descansar = nuevo_valor

    @property
    def fuerza(self):
        return self._fuerza

    @fuerza.setter
    def fuerza(self, new):
        self._fuerza = mantener_entre_extremos(1, 10, new)

    @property
    def suerte(self):
        return self._suerte

    @suerte.setter
    def suerte(self, new):
        self._suerte = mantener_entre_extremos(1, 10, new)

    @property
    def felicidad(self):
        return self._felicidad

    @felicidad.setter
    def felicidad(self, new):
        self._felicidad = mantener_entre_extremos(1, 10, new)

    @property
    def edad(self):
        return self._edad

    @edad.setter
    def edad(self, new):
        self._edad = mantener_entre_extremos(18, 60, new)

    @property
    def prob_item(self):
        '''
        define nueva probabilidad de encontrar item, si la arena es mojada esa porbabilidad
        siempre es 1, para cualquier otra la probabilidad toma el valor entregado
        '''
        return self._prob_item

    @prob_item.setter
    def prob_item(self, new):
        if type(self.arena) == ArenaMojada:
            self._prob_item = 1
        else:
            self._prob_item = new

    @property
    def arena(self):
        return self._arena

    @arena.setter
    def arena(self, new):
        self._arena = new
        self.prob_item = round(new.prob_item * (self.suerte / 10), 2)

    # bajo esta linea defino metodos 'normales'

    def descansar(self):
        if self.energia > 0:
            print('Todavia tiene energia!, no necesita descansar ;)')
        else:
            dias_descanso = int(self._edad / 20)
            self._dias_para_descansar = dias_descanso

    def encontrar_item(self):
        '''
        determina si un excavador encuentra un item, retorna el item si lo encuentra,
        retorna None si no encuentra nada
        '''
        encuentra = choices(['si', 'no'], [self.prob_item, 1 - self.prob_item], k=1)
        if encuentra[0] == 'no':
            return
        else:
            pesos_item = [self.arena.prob_consumible, self.arena.prob_tesoro]
            final = choices(['consumible', 'tesoro'], pesos_item, k=1)
            if final[0] == 'consumible':
                # creo una lista de todos los consumibles disponibles en la arena
                consumibles_disponibles = [
                    entry for entry in self.arena.items if entry.tipo == 'consumible'
                ]
                # eligo uno al azar y lo elimino de la lista general de la arena
                consumible_elegido = choice(consumibles_disponibles)
                self._arena.items.remove(consumible_elegido)
                return consumible_elegido
            elif final[0] == 'tesoro':
                tesoros_disponibles = [
                    entry for entry in self.arena.items if entry.tipo == 'tesoro'
                ]
                # eligo uno al azar y lo elimino de la lista general, de la arena
                tesoro_elegido = choice(tesoros_disponibles)
                self._arena.items.remove(tesoro_elegido)
                return tesoro_elegido

    # bajo esta linea defino los metodos abstractos

    @abstractmethod
    def cavar(self):
        '''
        retorna la cantidad de metros (float) que va a cavar este excavador
        '''
        metros = round(
            ((30 / self.edad) + ((self.felicidad + 2 * self.fuerza) / 10))
            * (1 / (10 * self.arena.dificultad)), 2)
        return metros

    @abstractmethod
    def gastar_energia(self):
        '''
        no retorna nada, calcula el gasto energetico y se lo resta a la energia del
        excavador
        '''
        gasto = int((10 / self.fuerza) + (self.edad / 6))
        self.energia -= gasto

    @abstractmethod
    def consumir(self, consumible):
        '''
        agrega los valores de los consumibles a los atributos del excavador,
        reajusta la prob_item a los nuevos valores de suerte, none return
        '''
        self.energia += consumible.energia
        self.fuerza += consumible.fuerza
        self.suerte += consumible.suerte
        self.felicidad += consumible.felicidad
        self.prob_item = self.arena.prob_item * (self.suerte / 10)


class ExcavadorDocencio(Excavador):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = 'Docencio'

    def cavar(self):
        self.felicidad += parametros.FELICIDAD_ADICIONAL_DOCENCIO
        self.fuerza += parametros.FUERZA_ADICIONAL_DOCENCIO
        return super().cavar()

    def gastar_energia(self):
        super().gastar_energia()
        self.energia -= parametros.ENERGIA_PERDIDA_DOCENCIO

    def consumir(self, consumible):
        super().consumir(consumible)


class ExcavadorTareo(Excavador):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = 'Tareo'

    def cavar(self):
        return super().cavar()

    def gastar_energia(self):
        super().gastar_energia()

    def consumir(self, consumible):
        super().consumir(consumible)
        self.energia += parametros.ENERGIA_ADICIONAL_TAREO
        self.suerte += parametros.SUERTE_ADICIONAL_TAREO
        self.edad += parametros.EDAD_ADICIONAL_TAREO
        self.felicidad -= parametros.FELICIDAD_PERDIDA_TAREO


class ExcavadorHibrido(ExcavadorDocencio, ExcavadorTareo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = 'Hibrido'

    def gastar_energia(self):
        '''
        incluye los cambios que se le hacen a la energia tanto en ExcavadorTareo
        como ExcavadorDocencio, el gasto energetico se reduce a la mitad
        '''
        gasto = int((10 / self.fuerza) + (self.edad / 6))
        self.energia -= (int(gasto / 2) + parametros.ENERGIA_PERDIDA_DOCENCIO)

    def consumir(self, consumible):
        return ExcavadorTareo.consumir(self, consumible)

    def cavar(self):
        return ExcavadorDocencio.cavar(self)

    @property
    def energia(self):
        return super().energia

    @energia.setter
    def energia(self, new):
        self._energia = mantener_entre_extremos(20, 100, new)
