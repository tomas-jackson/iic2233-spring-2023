from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from os.path import join


class VentanaInicio(QWidget):

    senal_cerrado = pyqtSignal(list)
    senal_inicio = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.con_error = False
        self.showing = False
        self.init_gui()

    def init_gui(self):
        self.setFixedSize(760, 760)
        self.setWindowTitle('DCCachos - Inicio')

        self.background_label = QLabel('', self)
        self.background_label.setFixedSize(760, 760)
        self.background_label.setScaledContents(True)

        self.logo_label = QLabel('', self)
        self.logo_label.setFixedSize(100, 63)
        self.logo_label.setScaledContents(True)
        self.logo_label.move(10, 0)
        # creo labels para cada user que recibiran el pixmap

        self.label_espera = QLabel('SALA DE ESPERA', self)
        font_espera = self.label_espera.font()
        font_espera.setBold(True)
        font_espera.setPointSize(40)
        self.label_espera.setFont(font_espera)
        self.label_espera.move(220, 100)
        self.label_espera.resize(self.label_espera.sizeHint())

        self.user1_label = QLabel('', self)
        self.user2_label = QLabel('', self)
        self.user3_label = QLabel('', self)
        self.user4_label = QLabel('', self)
        self.user_labels = [self.user1_label, self.user2_label, self.user3_label, self.user4_label]
        # modifico sus propiedades
        for i in range(len(self.user_labels)):
            self.user_labels[i].setFixedSize(150, 150)
            self.user_labels[i].setScaledContents(True)
            self.user_labels[i].move(20 + (i * 190), 340)

        self.user1_name = QLabel('Buscando...', self)
        self.user2_name = QLabel('Buscando...', self)
        self.user3_name = QLabel('Buscando...', self)
        self.user4_name = QLabel('Buscando...', self)
        self.user_names = [self.user1_name, self.user2_name, self.user3_name, self.user4_name]
        pos = 0
        for user in self.user_names:
            font = user.font()
            font.setBold(True)
            font.setPointSize(16)
            font.setFamily('Courier New')
            user.setFont(font)
            user.move(60 + (pos * 190), 500)
            pos += 1

        self.boton_iniciar = QPushButton('INICIO', self)
        self.boton_salir = QPushButton('SALIR!', self)

        self.boton_iniciar.resize(100, 30)
        self.boton_iniciar.clicked.connect(lambda x: self.senal_inicio.emit(['START']))
        self.boton_salir.resize(100, 30)
        self.boton_salir.clicked.connect(self.close)
        self.boton_salir.clicked.connect(lambda x: self.senal_cerrado.emit(['dc']))

        self.boton_iniciar.move(330, 700)
        self.boton_salir.move(330, 725)

    def actualizar_pixmaps_inicial(self, diccionario: dict) -> None:
        '''
        recibe una señal con el diccionario que contiene las rutas de los sprites
        y los actualiza en la gui
        '''
        for user in self.user_labels:
            user.setPixmap(QPixmap(join(*diccionario['avatar'])))
            user.resize(user.sizeHint())
        self.background_label.setPixmap(QPixmap(join(*diccionario['fondo_inicio'])))
        self.logo_label.setPixmap(QPixmap(join(*diccionario['logo'])))

    def actualizar_usuarios(self, usuarios: list):
        '''
        recibe los usuarios conectados y los muestra en ventana
        '''
        for i in range(len(usuarios)):
            self.user_names[i].setText(usuarios[i])
            self.user_names[i].resize(self.user_names[i].sizeHint())

    def closeEvent(self, event):
        if self.con_error is False:
            self.senal_cerrado.emit(['dc'])

    def abrir_popup_full(self):
        self.boton_iniciar.setEnabled(False)
        self.boton_salir.setEnabled(False)
        QMessageBox.warning(
            self, 'Lobby Completo', 'El lobby esta lleno, espera un cupo - NO CERRAR VENTANA')

    def abrir_popup_spot_found(self):
        self.boton_iniciar.setEnabled(True)
        self.boton_salir.setEnabled(True)
        QMessageBox.information(self, 'Espacio encontrado', 'Aviso - Espacio liberado, conectando')

    def abrir_popup_ingame(self):
        self.showing = True
        QMessageBox.information(
            self, 'Partida en curso', 'Ya hay una partida en curso, conectate mas tarde')
        self.close()

    def popup_dead_server(self):
        if self.isVisible() and self.showing is False:
            self.con_error = True
            QMessageBox.information(self, 'Desconectado', 'El servidor se desconecto - Saliendo')
            self.close()
