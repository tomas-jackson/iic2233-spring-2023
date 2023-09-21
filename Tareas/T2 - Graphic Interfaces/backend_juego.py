from backend_constructor import ProcesadorConstructor
from entidades import Luigi, FantasmaHorizontal, FantasmaVertical, Fuego, Pared, Roca, Estrella
import parametros
from PyQt5.QtCore import pyqtSignal, QTimer
import os
from copy import deepcopy


class ProcesadorJuego(ProcesadorConstructor):

    senal_constructor_juego = pyqtSignal()
    senal_can_luigi_move = pyqtSignal(bool)
    senal_rock_move = pyqtSignal(tuple, tuple, list)
    senal_actualizar_vidas = pyqtSignal(int)
    senal_reset_grilla = pyqtSignal(list)
    senal_sobre_estrella = pyqtSignal(bool)
    senal_juego_countdown = pyqtSignal(int)
    senal_muerte = pyqtSignal()
    senal_timeout = pyqtSignal()
    senal_muerte_fantasma = pyqtSignal()
    senal_cambio_direccion = pyqtSignal()
    senal_sacar_fantasma_mapa = pyqtSignal(tuple)
    senal_inicia_timer_fantasmas = pyqtSignal()
    senal_detener_timer_fantasmas = pyqtSignal()
    senal_cambiar_sprite_fantasma = pyqtSignal(tuple, tuple)
    senal_movimiento_valido_fant = pyqtSignal(tuple, tuple, str)
    senal_puntaje_final = pyqtSignal(str, float)
    senal_label_infinito = pyqtSignal(str)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tiempo_segundos = parametros.TIEMPO_CUENTA_REGRESIVA
        self.instancias = dict()
        self.timer_juego = QTimer()
        self.timer_juego.setInterval(1000)
        self.timer_juego.timeout.connect(self.actualizar_timer_juego)
        self.sobre_estrella = False
        self.vidas_gastadas = 1
        self.vidas_infinitas = False

    def conectar_fantasmas(self, instancia):
        instancia.senal_nueva_pos.connect(self.validar_nueva_pos_fantasma)
        self.senal_muerte_fantasma.connect(instancia.morir)
        self.senal_detener_timer_fantasmas.connect(instancia.morir)
        self.senal_cambio_direccion.connect(instancia.cambiar_direccion)
        self.senal_inicia_timer_fantasmas.connect(instancia.iniciar_timer)

    def leer_instanciar_clases(self):
        '''determina las instancias presentes en la grilla e inicializa
        la cantidad correspondiente de ellas, las almacena en un dict
        si encuentra a un fantasma, almacena su pos dentro de el y conecta sus
        metodos'''
        class_list = [Luigi, Estrella, FantasmaHorizontal, FantasmaVertical, Pared, Fuego, Roca]
        posiciones_h = []
        posiciones_v = []
        for class_id, actual_class in zip('LSHVPFR', class_list):
            self.instancias[class_id] = list()
            contador = 0
            for row in range(len(self.grilla)):
                contador += self.grilla[row].count(class_id)
                for col in range(len(self.grilla[0])):
                    if self.grilla[row][col] == 'H':
                        if (row, col) not in posiciones_h:
                            posiciones_h.append((row, col))
                    elif self.grilla[row][col] == 'V':
                        if (row, col) not in posiciones_v:
                            posiciones_v.append((row, col))
            for _ in range(contador):
                if class_id == 'H':
                    objeto = actual_class(posiciones_h.pop())
                    self.instancias[class_id].append(objeto)
                    self.conectar_fantasmas(objeto)
                elif class_id == 'V':
                    objeto = actual_class(posiciones_v.pop())
                    self.instancias[class_id].append(objeto)
                    self.conectar_fantasmas(objeto)
                else:
                    self.instancias[class_id].append(actual_class())

    def leer_grilla(self, archivo):
        path = os.path.join('mapas', archivo)
        with open(path, 'r', encoding='UTF-8') as mapa:
            map_info = [list(line.strip()) for line in mapa.readlines()]
        map_info.insert(0, list('B' * parametros.ANCHO_GRILLA))
        map_info.append(list('B' * parametros.ANCHO_GRILLA))
        for entry in map_info[1:len(map_info) - 1]:
            entry.insert(0, 'B')
            entry.append('B')

        self.grilla = map_info
        self.copia_grilla = deepcopy(map_info)
        self.leer_instanciar_clases()
        self.senal_grilla.emit(map_info)
        self.senal_inicia_timer_fantasmas.emit()

    def recibir_setear_grilla_inicio(self, grilla):
        self.grilla = grilla
        self.copia_grilla = deepcopy(self.grilla)
        self.leer_instanciar_clases()
        self.senal_grilla.emit(self.grilla)
        self.senal_constructor_juego.emit()
        self.senal_inicia_timer_fantasmas.emit()

    def resetear_grilla(self):
        self.grilla = deepcopy(self.copia_grilla)
        vidas_remaining = self.instancias['L'][0].vidas
        print(f'en resetear grilla vidas remaing {vidas_remaining}')
        self.leer_instanciar_clases()
        self.instancias['L'][0].vidas = vidas_remaining
        self.senal_reset_grilla.emit(self.copia_grilla)
        self.senal_inicia_timer_fantasmas.emit()

    def resetear_grilla_new_game(self):
        self.grilla = deepcopy(self.copia_grilla)
        self.leer_instanciar_clases()
        self.senal_reset_grilla.emit(self.copia_grilla)
        self.tiempo_segundos = parametros.TIEMPO_CUENTA_REGRESIVA
        self.iniciar_timer_juego()
        self.cambio_inicial_vidas()
        self.senal_inicia_timer_fantasmas.emit()
        self.vidas_gastadas = 1

    def validar_nueva_pos_luigi(self, old_coords, new_coords, increase):
        new_space = self.grilla[new_coords[0]][new_coords[1]]
        if new_space != '-':
            if new_space == 'R':
                if self.grilla[new_coords[0] + increase[0]][new_coords[1] + increase[1]] != '-':
                    self.senal_can_luigi_move.emit(False)
                else:
                    self.grilla[new_coords[0] + increase[0]][new_coords[1] + increase[1]] = 'R'
                    self.grilla[old_coords[0]][old_coords[1]] = '-'
                    self.grilla[new_coords[0]][new_coords[1]] = 'L'
                    self.senal_can_luigi_move.emit(True)
                    self.senal_rock_move.emit(new_coords, increase, self.grilla)
            elif new_space in 'FHV':
                if self.vidas_infinitas is False:
                    self.instancias['L'][0].vidas -= 1
                    self.vidas_gastadas += 1
                    self.senal_actualizar_vidas.emit(self.instancias['L'][0].vidas)
                self.senal_can_luigi_move.emit(False)
                self.resetear_grilla()
                if self.instancias['L'][0].vidas == -1:
                    self.senal_muerte.emit()
                    self.senal_detener_timer_fantasmas.emit()

            elif new_space == 'S':
                self.sobre_estrella = True
                self.senal_can_luigi_move.emit(True)
                self.senal_sobre_estrella.emit(True)
                self.enviar_puntaje()
                self.grilla[old_coords[0]][old_coords[1]] = '-'

            else:
                self.senal_can_luigi_move.emit(False)

        else:
            if self.sobre_estrella is not True:
                self.grilla[old_coords[0]][old_coords[1]] = '-'
                self.grilla[new_coords[0]][new_coords[1]] = 'L'
                self.senal_can_luigi_move.emit(True)
            else:
                self.sobre_estrella = False
                self.grilla[old_coords[0]][old_coords[1]] = 'S'
                self.grilla[new_coords[0]][new_coords[1]] = 'L'
                self.senal_can_luigi_move.emit(True)
                self.senal_sobre_estrella.emit(False)

    def cambio_inicial_vidas(self):
        self.senal_actualizar_vidas.emit(self.instancias['L'][0].vidas)

    def iniciar_timer_juego(self):
        self.timer_juego.start()
        self.timer_juego.singleShot(0, self.actualizar_timer_juego)

    def actualizar_timer_juego(self):
        if self.tiempo_segundos == 0:
            self.senal_timeout.emit()
            self.enviar_puntaje()
        self.senal_juego_countdown.emit(self.tiempo_segundos)
        if self.vidas_infinitas is not True:
            self.tiempo_segundos -= 1

    def cambiar_estado_pausa(self, booleano):
        if booleano is True:
            self.timer_juego.stop()
            self.senal_detener_timer_fantasmas.emit()

        else:
            self.timer_juego.start()
            self.senal_inicia_timer_fantasmas.emit()

    def validar_nueva_pos_fantasma(self, old_pos, new_pos):
        fantasma = self.sender()
        ghost_id = fantasma.id
        new_space = self.grilla[new_pos[0]][new_pos[1]]
        if new_space != '-':
            if new_space == 'F':
                fantasma.morir()
                self.senal_sacar_fantasma_mapa.emit(old_pos)
                self.grilla[old_pos[0]][old_pos[1]] = '-'

            elif new_space == 'S':
                fantasma.on_star = True
                self.grilla[old_pos[0]][old_pos[1]] = '-'
                self.grilla[new_pos[0]][new_pos[1]] = ghost_id
                fantasma.pos = new_pos
                self.senal_movimiento_valido_fant.emit(old_pos, new_pos, fantasma.id)

            elif new_space == 'L':
                if self.vidas_infinitas is not True:
                    self.instancias['L'][0].vidas -= 1
                    self.vidas_gastadas += 1
                    self.senal_actualizar_vidas.emit(self.instancias['L'][0].vidas)
                    self.senal_can_luigi_move.emit(False)
                self.resetear_grilla()
                if self.instancias['L'][0].vidas == -1:
                    self.senal_muerte.emit()
                    self.senal_detener_timer_fantasmas.emit()
                    self.enviar_puntaje()
            else:
                if fantasma.direccion is True:
                    fantasma.direccion = False
                else:
                    fantasma.direccion = True
        else:
            if fantasma.on_star is True:
                self.grilla[old_pos[0]][old_pos[1]] = 'S'
                self.grilla[new_pos[0]][old_pos[1]] = ghost_id
                fantasma.on_star = False
                self.senal_movimiento_valido_fant.emit(old_pos, new_pos, fantasma.id)

            else:
                self.grilla[old_pos[0]][old_pos[1]] = '-'
                self.grilla[new_pos[0]][new_pos[1]] = ghost_id
                self.senal_movimiento_valido_fant.emit(old_pos, new_pos, fantasma.id)
            
            fantasma.pos = new_pos

    def iniciar_timer_fantasma(self):
        self.senal_inicia_timer_fantasmas.emit()

    def setear_user(self, user):
        self.user = user

    def calcular_puntaje(self):
        if self.vidas_infinitas is True:
            puntaje = (parametros.TIEMPO_CUENTA_REGRESIVA * parametros.MULTIPLICADOR_PUNTAJE)
        
        else:
            tiempo_restante = self.tiempo_segundos
            puntaje = (tiempo_restante * parametros.MULTIPLICADOR_PUNTAJE) / self.vidas_gastadas

        return puntaje

    def enviar_puntaje(self):
        puntaje = self.calcular_puntaje()
        self.senal_puntaje_final.emit(self.user, puntaje)

    def genocidio(self):
        for fantasma in (self.instancias['H'] + self.instancias['V']):
            fantasma.morir()
            self.grilla[fantasma.pos[0]][fantasma.pos[1]] = '-'
            self.senal_sacar_fantasma_mapa.emit(fantasma.pos)

    def setear_vidas_infinitas(self):
        self.vidas_infinitas = True
        self.senal_label_infinito.emit('INFINITAS')
