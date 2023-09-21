'''
inlcuye a todas las clases que modelan a las distintas entidades del juego
'''
import parametros
from random import uniform
from PyQt5.QtCore import QTimer, pyqtSignal, QObject


class Luigi:
    def __init__(self):
        self.vidas = parametros.CANTIDAD_VIDAS
        self.id = 'L'
        # quiza agregarle a cada objeto si puede chocar o no con otro


class FantasmaVertical(QObject):

    maximo = parametros.MAXIMO_FANTASMAS_VERTICAL
    senal_nueva_pos = pyqtSignal(tuple, tuple)

    def __init__(self, pos=(0, 0)):
        super().__init__()
        FantasmaVertical.maximo -= 1
        self.id = 'V'
        self.pond_velocidad_fantasmas = uniform(parametros.MIN_VELOCIDAD, parametros.MAX_VELOCIDAD)
        self.tiempo_movimiento_fantasmas = 1 / self.pond_velocidad_fantasmas
        self.timer = QTimer()
        self.direccion = True  # True = subir, False = bajar
        self.timer.timeout.connect(self.moverse)
        self.pos = pos
        self.on_ghost = False
        self.on_star = False

    def iniciar_timer(self):
        self.timer.start(int(1000 * self.tiempo_movimiento_fantasmas))

    def moverse(self):
        if self.direccion is True:
            new_pos = (self.pos[0] - 1, self.pos[1])
            self.senal_nueva_pos.emit(self.pos, new_pos)
        else:
            new_pos = (self.pos[0] + 1, self.pos[1])
            self.senal_nueva_pos.emit(self.pos, new_pos)

    def cambiar_direccion(self):
        if self.direccion is True:
            self.direccion = False
        else:
            self.direccion = True

    def morir(self):
        self.timer.stop()


class FantasmaHorizontal(QObject):

    maximo = parametros.MAXIMO_FANTASMAS_HORIZONTAL
    senal_nueva_pos = pyqtSignal(tuple, tuple)

    def __init__(self, pos=(0, 0)):
        super().__init__()
        FantasmaHorizontal.maximo -= 1
        self.id = 'H'
        self.pond_velocidad_fantasmas = uniform(parametros.MIN_VELOCIDAD, parametros.MAX_VELOCIDAD)
        self.tiempo_movimiento_fantasmas = 1 / self.pond_velocidad_fantasmas
        self.timer = QTimer()
        self.direccion = True  # True = subir, False = bajar
        self.timer.timeout.connect(self.moverse)
        self.pos = pos
        self.on_ghost = False
        self.on_star = False

    def iniciar_timer(self):
        self.timer.start(int(1000 * self.tiempo_movimiento_fantasmas))

    def moverse(self):
        if self.direccion is True:
            new_pos = (self.pos[0], self.pos[1] + 1)
            self.senal_nueva_pos.emit(self.pos, new_pos)
        else:
            new_pos = (self.pos[0], self.pos[1] - 1)
            self.senal_nueva_pos.emit(self.pos, new_pos)

    def cambiar_direccion(self):
        if self.direccion is True:
            self.direccion = False
        else:
            self.direccion = True

    def morir(self):
        self.timer.stop()


class Pared:

    maximo = parametros.MAXIMO_PARED

    def __init__(self):
        Pared.maximo -= 1
        self.inamovible = True
        self.impenetrable = True
        self.damage = False
        self.id = 'P'


class Roca:

    maximo = parametros.MAXIMO_ROCA

    def __init__(self):
        Roca.maximo -= 1
        self.inamovible = False
        self.impenetrable = True
        self.damage = False
        self.id = 'R'


class Fuego:

    maximo = parametros.MAXIMO_FUEGO

    def __init__(self):
        Fuego.maximo -= 1
        self.inamovible = True
        self.impenetrable = False
        self.damage = True
        self.id = 'F'


class Estrella:
    def __init__(self) -> None:
        self.id = 'S'
