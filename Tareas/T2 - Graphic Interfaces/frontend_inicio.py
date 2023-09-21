"""
este archivo maneja el front-end de la ventana de inicio del juego,
solo inicializando sus secciones graficas
"""
import parametros
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox, QPushButton
from PyQt5.QtGui import QPixmap


class VentanaUserInvalid(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()

    def init_gui(self):
        self.setFixedSize(400, 200)
        self.move(200, 200)
        self.setWindowTitle('Usuario Invalido!!!!')

    def cambiar_label(self, errores):
        '''recibe errores de nombre de usuario en la ventana de inicio y
        genera la ventana que muestra cuales fueron'''

        layout = QHBoxLayout()
        self.error_label = QLabel('Nombre invalido!, revisa tus errores:', self)
        layout.addStretch(1)
        layout.addWidget(self.error_label)
        layout.addStretch(1)
        self.error_label.resize(self.error_label.sizeHint())
        if errores[0] is True:
            self.label_largo = QLabel('Longitud correcta: ✅')
        elif errores[0] is False:
            self.label_largo = QLabel('Longitud correcta: ❌')
        if errores[1] is True:
            self.label_alnum = QLabel('Solo incluye letras y numeros: ✅')
        elif errores[1] is False:
            self.label_alnum = QLabel('Solo incluye letras y numeros: ❌')
        if errores[2] is True:
            self.label_void = QLabel('Nombre no vacio: ✅')
        elif errores[2] is False:
            self.label_void = QLabel('Nombre no vacio: ❌')
        lay_vertical = QVBoxLayout()
        lay_vertical.addLayout(layout)
        lay_vertical.addWidget(self.label_largo)
        lay_vertical.addWidget(self.label_alnum)
        lay_vertical.addWidget(self.label_void)
        self.setLayout(lay_vertical)
        self.boton_cierre = QPushButton('Cerrar', self)
        self.boton_cierre.clicked.connect(self.close)
        self.boton_cierre.resize(self.boton_cierre.sizeHint())
        self.boton_cierre.move(250, 150)


class VentanaInicio(QWidget):

    senal_inicio = pyqtSignal(list)
    senal_ventana_error = pyqtSignal(list)
    senal_iniciar_constructor = pyqtSignal()
    senal_iniciar_juego = pyqtSignal()
    senal_enviar_user = pyqtSignal(str)
    senal_enviar_map_name = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.iniciar_gui()

    def iniciar_gui(self):

        # defino dimensiones del widget principal y le pongo el fondo de background image
        self.setFixedSize(600, 680)
        self.move(100, 100)
        self.setWindowTitle('DCCazaFantasmas! - Inicio')

        # defino el pixmap y label que seran el fondo
        fondo = QPixmap(parametros.PATH_INICIO_FONDO)
        self.label_fondo = QLabel(self)
        self.label_fondo.setGeometry(0, 0, 600, 680)
        self.label_fondo.setPixmap(fondo)

        # defino los widgets de la linea que va a recibir la entrada del user name
        layout_user = QHBoxLayout()
        self.label_user = QLabel('Username: ', self)
        self.label_user.resize(self.label_user.sizeHint())
        self.label_user.setStyleSheet('color: white')
        self.line_edit_user = QLineEdit()
        self.line_edit_user.resize(self.line_edit_user.sizeHint())
        self.boton_confirm_user = QPushButton
        layout_user.addStretch(1)
        layout_user.addWidget(self.label_user)
        layout_user.addWidget(self.line_edit_user)
        layout_user.addStretch(1)

        # defino los widgets del header que contiene el logo
        header = QHBoxLayout()
        self.label_logo = QLabel('', self)
        self.label_logo.setMinimumHeight(95)
        self.label_logo.setMaximumHeight(95)
        self.label_logo.setMinimumWidth(518)
        self.label_logo.setMaximumHeight(518)
        pix_logo = QPixmap(parametros.PATH_LOGO)
        self.label_logo.setPixmap(pix_logo)
        header.addStretch(1)
        header.addWidget(self.label_logo)
        header.addStretch(1)

        # defino los widgets de la seleccion de mapa
        layout_mapa = QHBoxLayout()
        self.label_mapa = QLabel(' Elige mapa: ', self)
        self.label_mapa.resize(self.label_mapa.sizeHint())
        self.label_mapa.setStyleSheet('color: white')
        self.combo_box = QComboBox()
        layout_mapa.addStretch(1)
        layout_mapa.addWidget(self.label_mapa)
        layout_mapa.addWidget(self.combo_box)
        layout_mapa.addStretch(1)

        # defino el boton de inicio
        self.start_button = QPushButton('&Start', self)
        self.start_button.resize(self.start_button.sizeHint())

        # defino el boton de salida, lo conecto a self.close()
        self.exit_button = QPushButton('&Exit', self)
        self.exit_button.resize(self.exit_button.sizeHint())
        self.exit_button.clicked.connect(self.close)

        # agrego todo a un layout vertical
        layout_principal = QVBoxLayout()
        layout_principal.addLayout(header)
        layout_principal.addStretch(1)
        layout_principal.addLayout(layout_user)
        layout_principal.addStretch(1)
        layout_principal.addLayout(layout_mapa)
        layout_principal.addStretch(1)
        layout_principal.addWidget(self.start_button)
        layout_principal.addWidget(self.exit_button)

        # desplego el vertical
        self.setLayout(layout_principal)

        # defino conexiones
        self.start_button.clicked.connect(self.start_clicked)

    def start_clicked(self):
        '''
        envia, mediante 'senal_inicio', el username y mapa actualmente seleccionado
        al backend de la ventana de inicio
        '''
        self.senal_inicio.emit([self.line_edit_user.text(), self.combo_box.currentText()])

    def actualizar_combo_box(self, lista_mapas):
        '''
        recibe la lista de mapas de la señal 'senal_info_mapa' y se la agrega
        al combobox
        '''
        self.combo_box.addItems(lista_mapas + ['Mapa Vacio (constructor)'])

    def iniciar_partida(self, data):
        '''
        recibe el username y nombre de mapa procesados por el backend mediante
        senal_start del backend, si no es valido abre ventana de error
        si es valido y el mapa es vacio, abre constructor
        en otro caso abre modo juego
        '''
        if False in data[0]:
            self.ventana_error = VentanaUserInvalid()
            self.senal_ventana_error.connect(self.ventana_error.cambiar_label)
            self.senal_ventana_error.emit(data[0])
            self.ventana_error.show()
        elif 'Mapa Vacio' in data[1]:
            self.senal_iniciar_constructor.emit()
            self.senal_enviar_user.emit(self.line_edit_user.text())
        else:
            self.senal_iniciar_juego.emit()
            self.senal_enviar_user.emit(self.line_edit_user.text())
            self.senal_enviar_map_name.emit(data[1])
