'''
en este archivo se lleva a cabo el backend del constructor,
clases correspondientes
'''
from entidades import Luigi, FantasmaHorizontal, FantasmaVertical, Fuego, Pared, Roca, Estrella
import parametros
from PyQt5.QtCore import QObject, pyqtSignal


class ProcesadorConstructor(QObject):

    senal_grilla = pyqtSignal(list)
    senal_cant_disponible = pyqtSignal(dict)
    senal_ventana_error_pos = pyqtSignal()
    senal_enviar_grilla_juego = pyqtSignal(list)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ancho = parametros.ANCHO_GRILLA
        largo = parametros.LARGO_GRILLA
        self.user = user
        self.grilla = [
            ['-' for _ in range(parametros.ANCHO_GRILLA)] for _ in range(parametros.LARGO_GRILLA)
            ]
        for row in range(len(self.grilla)):
            for col in range(len(self.grilla[0])):
                if row in [0, largo - 1] or col in [0, ancho - 1]:
                    self.grilla[row][col] = 'B'

        # instancio los objetos en un diccionario para referenciar cantidades
        clases = [Pared, Fuego, FantasmaHorizontal, FantasmaVertical, Roca]
        self.entidades = dict()
        self.entidades['L'] = [Luigi()]
        self.entidades['S'] = [Estrella()]
        for class_id, class_object in zip('PFHVR', clases):
            self.instanciar_clase(class_object, class_id)

    def instanciar_clase(self, clase, id_class):
        '''
        instancia todas las clases que tienen un maximo de cantidad
        las almacena en el dict de la clase procesador self.entidades
        no return
        '''
        self.entidades[id_class] = list()
        while clase.maximo > 0:
            self.entidades[id_class].append(clase())

    def enviar_grilla(self):
        '''emito 'senal_grilla' que envia los contenidos de la grilla
        actual al frontend para que sea procesado y transformada al
        QGridLayout de la ventana'''
        self.senal_grilla.emit(self.grilla)

    def enviar_instancias_disponibles(self):
        '''envia el diccionario que contiene a todas las entidades
        disponibles para insertar a la grilla, lo hace mediante la señal
        'senal_cant_disponible'
        '''
        self.senal_cant_disponible.emit(self.entidades)

    def procesar_enviar_boton_seteado(self, boton_id, coord):
        '''recibe la posicion y el id del boton soltado, si la posicion es valida
        para insertar en la grilla (no esta bloqueada) reduce en uno las entidades
        disponibles de ese tipo, modifica la grilla en las coordenadas entregadas.
        Finalmente emite señales para actualizar la grilla y las cantidades disponibles
        en el frontend. En otro caso emite una señal para abrir la ventana de error'''
        if len(self.entidades[boton_id]) > 0 and self.grilla[coord[0]][coord[1]] == '-':
            clase = self.entidades[boton_id].pop()
            self.grilla[coord[0]][coord[1]] = boton_id
            if boton_id in 'HV':
                clase.pos = coord
        elif self.grilla[coord[0]][coord[1]] != '-':
            self.senal_ventana_error_pos.emit()
        self.enviar_instancias_disponibles()
        self.enviar_grilla()

    def limpiar_grilla(self):
        '''si el front end envia la orden de limpiar, este metodo reinicia grilla
        y cantidades, las envia devuelta al frontend'''
        ancho = parametros.ANCHO_GRILLA
        largo = parametros.LARGO_GRILLA
        self.grilla = [['-' for _ in range(ancho)] for _ in range(largo)]
        for row in range(len(self.grilla)):
            for col in range(len(self.grilla[0])):
                if row in [0, largo - 1] or col in [0, ancho - 1]:
                    self.grilla[row][col] = 'B'
        Pared.maximo = parametros.MAXIMO_PARED
        Fuego.maximo = parametros.MAXIMO_FUEGO
        FantasmaHorizontal.maximo = parametros.MAXIMO_FANTASMAS_HORIZONTAL
        FantasmaVertical.maximo = parametros.MAXIMO_FANTASMAS_VERTICAL
        Roca.maximo = parametros.MAXIMO_ROCA
        clases = [Pared, Fuego, FantasmaHorizontal, FantasmaVertical, Roca]
        self.entidades = dict()
        self.entidades['L'] = [Luigi()]
        self.entidades['S'] = [Estrella()]
        for class_id, class_object in zip('PFHVR', clases):
            self.instanciar_clase(class_object, class_id)
        self.enviar_grilla()
        self.enviar_instancias_disponibles()

    def setear_user(self, user):
        '''este metodo setea el username entregado por el usuario en la ventana
        de inicio'''
        self.user = user

    def enviar_grilla_inicio_juego(self):
        self.senal_enviar_grilla_juego.emit(self.grilla)
