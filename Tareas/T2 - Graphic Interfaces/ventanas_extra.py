from PyQt5.QtCore import pyqtSignal, QUrl
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtMultimedia import QSoundEffect
import parametros as p


class VentanaVictoria(QWidget):

    senal_reinicio = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle('VICTORIA!!!11!!!11111!1!')
        layout = QHBoxLayout()
        layout.addStretch(1)
        self.label_info = QLabel('placeholder', self)
        layout.addWidget(self.label_info)
        layout.addStretch(1)

        self.boton_salir = QPushButton('&Salir', self)
        self.boton_jugar_again = QPushButton('&Jugar de nuevo', self)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.boton_jugar_again)
        vlayout.addWidget(self.boton_salir)
        layout.addLayout(vlayout)
        self.setLayout(layout)

        self.audio = QSoundEffect(self)
        self.audio.setSource(QUrl.fromLocalFile(p.RUTA_AUDIO_WIN))

    def showEvent(self, e):
        super(VentanaVictoria, self).showEvent(e)
        self.audio.play()


class VentanaTimeout(QWidget):

    senal_reinicio = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle('Perdiste - sin tiempo')
        layout = QHBoxLayout()
        layout.addStretch(1)
        self.label_info = QLabel('placeholder', self)
        layout.addWidget(self.label_info)
        layout.addStretch(1)

        self.boton_salir = QPushButton('&Salir', self)
        self.boton_jugar_again = QPushButton('&Jugar de nuevo', self)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.boton_jugar_again)
        vlayout.addWidget(self.boton_salir)
        layout.addLayout(vlayout)
        self.setLayout(layout)

        self.audio = QSoundEffect(self)
        self.audio.setSource(QUrl.fromLocalFile(p.RUTA_AUDIO_LOSE))

    def showEvent(self, e):
        super(VentanaTimeout, self).showEvent(e)
        self.audio.play()


class VentanaMuerte(QWidget):

    senal_reinicio = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle('Perdiste - sin vidas')
        layout = QHBoxLayout()
        layout.addStretch(1)
        self.label_info = QLabel('placeholder', self)
        layout.addWidget(self.label_info)
        layout.addStretch(1)

        self.boton_salir = QPushButton('&Salir', self)
        self.boton_jugar_again = QPushButton('&Jugar de nuevo', self)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.boton_jugar_again)
        vlayout.addWidget(self.boton_salir)
        layout.addLayout(vlayout)
        self.setLayout(layout)

        self.audio = QSoundEffect(self)
        self.audio.setSource(QUrl.fromLocalFile(p.RUTA_AUDIO_LOSE))

    def showEvent(self, e):
        super(VentanaMuerte, self).showEvent(e)
        self.audio.play()
