
import parametros as p
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap
from copy import deepcopy
from ventanas_extra import VentanaMuerte, VentanaTimeout, VentanaVictoria


class VentanaJuego(QWidget):

    senal_validar_luigi = pyqtSignal(tuple, tuple, tuple)
    senal_cambiar_pausa = pyqtSignal(bool)
    senal_new_game = pyqtSignal()
    senal_orden_puntaje = pyqtSignal()
    senal_vidas_infinitas = pyqtSignal()
    senal_genocidio = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.botones_apretados = set()
        self.setAcceptDrops(True)
        self.estado_pausa = False
        self.puntaje = None
        self.init_gui()

    def init_gui(self):
        # defino dimensiones principales y titulo
        self.setWindowTitle('DCazaFantasmas! - Juego')
        self.setFixedSize(600, 560)

        # creo boton de pausa
        self.boton_pausa = QPushButton('&Pausar', self)
        self.boton_pausa.clicked.connect(self.cambiar_pausa)
        self.label_vidas = QLabel(f'Vidas: {p.CANTIDAD_VIDAS}', self)
        self.label_temporizador = QLabel('Tiempo: 420.69')
        # creo el layout de la mitad izquierda
        self.left_vlayout = QVBoxLayout()

        self.limpiar_fake = QPushButton('&Limpiar', self)
        self.limpiar_fake.setEnabled(False)
        self.start_fake = QPushButton('&Iniciar', self) 
        self.start_fake.setEnabled(False)

        # agrego botones de entrada y salida
        self.left_vlayout.addWidget(self.boton_pausa)
        self.left_vlayout.addWidget(self.label_vidas)
        self.left_vlayout.addWidget(self.label_temporizador)
        self.left_vlayout.addStretch(1)
        self.left_vlayout.addWidget(self.start_fake)
        self.left_vlayout.addWidget(self.limpiar_fake)

        # creo layout global
        placeholder = QGridLayout()
        self.layout_global = QHBoxLayout()
        self.layout_global.addLayout(self.left_vlayout)
        self.layout_global.addLayout(placeholder)  # el gridlayout es un placeholder
        self.setLayout(self.layout_global)

    def receive_set_grilla(self, grilla):
        widgets = []
        item = self.layout_global.takeAt(1)
        layout_delete = item.layout()
        layout_delete.deleteLater()
        QApplication.processEvents()
        new_grilla = QGridLayout()
        for row in range(len(grilla)):
            for col in range(len(grilla[0])):
                label = QLabel('', self)
                label.setFixedSize(32, 32)
                label.setAcceptDrops(True)
                label_fondo = QLabel('', self)
                label_fondo.setFixedSize(32, 32)
                label_fondo.setAcceptDrops(True)
                label_fondo.setStyleSheet('background-color: black')
                if grilla[row][col] != 'S':
                    new_grilla.addWidget(label_fondo, row, col)
                # perdon por estas lineas querido ayudante
                if grilla[row][col] == 'B':
                    label.setPixmap(QPixmap(p.PATH_BORDE))
                    label.setStyleSheet('')
                    new_grilla.addWidget(label, row, col)

                if grilla[row][col] == 'L':
                    self.posicion_luigi = (row, col)
                    self.posicion_luigi_copia = (row, col)

                if grilla[row][col] == 'P':
                    label.setPixmap(QPixmap(p.RUTA_WALL))
                    label.setStyleSheet('')
                    new_grilla.addWidget(label, row, col)

                if grilla[row][col] == 'F':
                    label.setPixmap(QPixmap(p.RUTA_FIRE))
                    new_grilla.addWidget(label, row, col)

                if grilla[row][col] == 'R':
                    label.setPixmap(QPixmap(p.RUTA_ROCK))
                    new_grilla.addWidget(label, row, col)

                if grilla[row][col] == 'H':
                    label.setPixmap(QPixmap(p.RUTA_FANTASMA_HORIZONTAL))
                    new_grilla.addWidget(label, row, col)

                if grilla[row][col] == 'V':
                    label.setPixmap(QPixmap(p.RUTA_FANTASMA_VERTICAL))
                    new_grilla.addWidget(label, row, col)

                if grilla[row][col] == 'S':
                    label.setPixmap(QPixmap(p.RUTA_STAR))
                    label.setScaledContents(True)
                    label.setStyleSheet('background-color: black')
                    new_grilla.addWidget(label, row, col)

                widgets.append(label)

        self.luigi = QLabel('L', self)
        self.luigi.setPixmap(QPixmap(p.RUTA_LUIGI))
        self.luigi.setFixedSize(32, 32)
        self.luigi.setAcceptDrops(True)
        new_grilla.addWidget(self.luigi, self.posicion_luigi[0], self.posicion_luigi[1])
        new_grilla.setSpacing(0)
        self.layout_global.addLayout(new_grilla)
        for widget in widgets:
            widget.raise_()
        self.luigi.raise_()

    def cambiar_estado_movimiento_luigi(self, booleano):
        self.luigi_movible = booleano

    def cambiar_sobre_estrella(self, booleano):
        self.on_star = booleano

    def cambiar_estado_movimiento_roca(self, booleano):
        self.roca_movible = booleano

    def actualizar_label_vidas(self, vidas):
        self.label_vidas.setText(f'Vidas: {vidas}')

    def keyPressEvent(self, event) -> None:
        grilla = self.layout_global.itemAt(1).layout()
        row = self.posicion_luigi[0]
        col = self.posicion_luigi[1]
        self.botones_apretados.add(event.key())
        if event.key() == Qt.Key_P:
            self.cambiar_pausa()
        if self.estado_pausa is False:
            if event.key() == Qt.Key_W:
                increase = (-1, 0)
                new_coords = (row - 1, col)
                self.senal_validar_luigi.emit(self.posicion_luigi, new_coords, increase)
                if self.luigi_movible is True:
                    row -= 1

            if event.key() == Qt.Key_A:
                increase = (0, -1)
                new_coords = (row, col - 1)
                self.senal_validar_luigi.emit(self.posicion_luigi, new_coords, increase)
                if self.luigi_movible is True:
                    col -= 1

            if event.key() == Qt.Key_S:
                increase = (1, 0)
                new_coords = (row + 1, col)
                self.senal_validar_luigi.emit(self.posicion_luigi, new_coords, increase)
                if self.luigi_movible is True:
                    row += 1

            if event.key() == Qt.Key_D:
                increase = (0, 1)
                new_coords = (row, col + 1)
                self.senal_validar_luigi.emit(self.posicion_luigi, new_coords, increase)
                if self.luigi_movible is True:
                    col += 1

        self.posicion_luigi = (row, col)
        grilla.addWidget(self.luigi, row, col)

        if event.key() == Qt.Key_G:
            if self.on_star is True:
                self.senal_orden_puntaje.emit()
                self.abrir_ventana_ganaste()

        if (Qt.Key_I in self.botones_apretados
                and Qt.Key_N in self.botones_apretados
                and Qt.Key_F in self.botones_apretados):
            self.senal_vidas_infinitas.emit()

        if (Qt.Key_K in self.botones_apretados
                and Qt.Key_I in self.botones_apretados
                and Qt.Key_L in self.botones_apretados):
            self.senal_genocidio.emit()

    def keyReleaseEvent(self, event):
        self.botones_apretados.remove(event.key())

    def mover_roca(self, pos, increase, grilla):
        grilla = self.layout_global.itemAt(1).layout()
        fondo = grilla.itemAtPosition(pos[0], pos[1]).widget()
        fondo = grilla.takeAt(grilla.indexOf(fondo)).widget()
        old_rock = grilla.itemAtPosition(pos[0], pos[1]).widget()
        old_rock.deleteLater()
        QApplication.processEvents()
        if grilla.indexOf(old_rock) != -1:
            grilla.removeWidget(old_rock)
        grilla.addWidget(fondo, pos[0], pos[1])
        new_rock = QLabel('', self)
        new_rock.setFixedSize(32, 32)
        new_rock.setPixmap(QPixmap(p.RUTA_ROCK))
        grilla.addWidget(new_rock, pos[0] + increase[0], pos[1] + increase[1])
        new_rock.raise_()
        self.luigi.raise_()

    def resetear(self, grilla):
        self.receive_set_grilla(grilla)
        self.estado_pausa = False
        QTimer.singleShot(1, self.resetear_luigi)

    def resetear_luigi(self):
        self.luigi.deleteLater()
        self.posicion_luigi = deepcopy(self.posicion_luigi_copia)
        new_luigi = QLabel('L', self)
        new_luigi.setFixedSize(32, 32)
        new_luigi.setPixmap(QPixmap(p.RUTA_LUIGI))
        layout = self.layout_global.itemAt(1).layout()
        layout.addWidget(new_luigi, self.posicion_luigi[0], self.posicion_luigi[1])
        self.luigi = new_luigi

    def actualizar_countdown(self, tiempo_restante):
        self.label_temporizador.setText(f'Tiempo: {tiempo_restante} s.')

    def cambiar_pausa(self):
        if self.estado_pausa is True:
            self.senal_cambiar_pausa.emit(False)
            self.estado_pausa = False
        else:
            self.senal_cambiar_pausa.emit(True)
            self.estado_pausa = True

    def sacar_fantasma(self, pos):
        grilla = self.layout_global.itemAt(1).layout()
        fondo = grilla.itemAtPosition(pos[0], pos[1]).widget()
        fondo = grilla.takeAt(grilla.indexOf(fondo)).widget()
        fantasma = grilla.itemAtPosition(pos[0], pos[1]).widget()
        fantasma.deleteLater()
        QApplication.processEvents()
        if grilla.indexOf(fantasma) != -1:
            grilla.removeWidget(fantasma)
        grilla.addWidget(fondo, pos[0], pos[1])

    def mover_fantasma(self, old_pos, new_pos, ghost_id):
        self.sacar_fantasma(old_pos)
        grilla = self.layout_global.itemAt(1).layout()
        new_fantasma = QLabel('', self)
        new_fantasma.setFixedSize(32, 32)
        if ghost_id == 'H':
            pix = QPixmap(p.RUTA_FANTASMA_HORIZONTAL)
            new_fantasma.setPixmap(pix)
        elif ghost_id == 'V':
            pix = QPixmap(p.RUTA_FANTASMA_VERTICAL)
            new_fantasma.setPixmap(pix)

        grilla.addWidget(new_fantasma, new_pos[0], new_pos[1])

    def actualizar_puntaje(self, user, puntaje):
        self.puntaje = puntaje
        self.user = user

    def abrir_ventana_muerte(self):
        self.cambiar_pausa()
        self.ventana = VentanaMuerte()
        self.senal_orden_puntaje.emit()
        text1 = f'Usuario: {self.user} - '
        text2 = f'MORISTE - SKILL ISSUE - PUNTOS: {round(self.puntaje, 2)}'
        self.ventana.label_info.setText(text1 + text2)
        self.ventana.boton_salir.clicked.connect(self.close)
        self.ventana.boton_salir.clicked.connect(self.ventana.close)
        self.ventana.boton_jugar_again.clicked.connect(lambda: self.senal_new_game.emit())
        self.ventana.boton_jugar_again.clicked.connect(self.ventana.close)
        self.ventana.show()

    def abrir_ventana_ganaste(self):
        self.cambiar_pausa()
        self.ventana = VentanaVictoria()
        self.senal_orden_puntaje.emit()
        text1 = f'Usuario: {self.user} - '
        text2 = f'GANASTEEEeeEEEEEeeEe - PUNTAJE: {round(self.puntaje, 2)}'
        self.ventana.label_info.setText(text1 + text2)
        self.ventana.boton_salir.clicked.connect(self.close)
        self.ventana.boton_salir.clicked.connect(self.ventana.close)
        self.ventana.boton_jugar_again.clicked.connect(lambda: self.senal_new_game.emit())
        self.ventana.boton_jugar_again.clicked.connect(self.ventana.close)
        self.ventana.show()

    def abrir_ventana_timeout(self):
        self.cambiar_pausa()
        self.ventana = VentanaTimeout()
        self.senal_orden_puntaje.emit()
        text1 = f'Usuario: {self.user} - '
        text2 = f'SIN TIEMPO - TIEMPO PERDISTE - PUNTAJE: {round(self.puntaje, 2)}'
        self.ventana.label_info.setText(text1 + text2)
        self.ventana.boton_salir.clicked.connect(self.close)
        self.ventana.boton_salir.clicked.connect(self.ventana.close)
        self.ventana.boton_jugar_again.clicked.connect(lambda: self.senal_new_game.emit())
        self.ventana.boton_jugar_again.clicked.connect(self.ventana.close)
        self.ventana.show()
