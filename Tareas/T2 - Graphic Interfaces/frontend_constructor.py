import parametros as p
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon
from widgets_custom import BotonArrastable


class VentanaErrorPosicion(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle('Error')
        self.setFixedSize(400, 200)
        self.move(400, 400)

        self.mensaje_error = QLabel('NO! - Esta posicion ya se esta utilizando', self)
        self.mensaje_error.resize(self.mensaje_error.sizeHint())
        self.mensaje_error.move(75, 75)

        self.boton_salir = QPushButton('&Entendido', self)
        self.boton_salir.resize(self.boton_salir.sizeHint())
        self.boton_salir.move(200, 150)
        self.boton_salir.clicked.connect(self.close)


class VentanaFaltaLuigi(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle('Error')
        self.setFixedSize(400, 200)
        self.move(400, 400)

        self.mensaje_error = QLabel('NO! - Falta Luigi y/o una estrella en el mapa', self)
        self.mensaje_error.resize(self.mensaje_error.sizeHint())
        self.mensaje_error.move(75, 75)

        self.boton_salir = QPushButton('&Entendido', self)
        self.boton_salir.resize(self.boton_salir.sizeHint())
        self.boton_salir.move(200, 150)
        self.boton_salir.clicked.connect(self.close)


class VentanaConstructor(QWidget):

    senal_actualizar_cantidad = pyqtSignal()
    senal_boton_seteado = pyqtSignal(str, tuple)
    senal_limpiar_grilla = pyqtSignal()
    senal_iniciar_juego = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.init_gui()

    def init_gui(self):
        # defino dimensiones principales y titulo
        self.setWindowTitle('DCazaFantasmas! - Constructor')
        self.setFixedSize(600, 560)

        # creo el combobox que va a tener los tipos de elementos en el y conecto la senal
        self.type_combobox = QComboBox(self)
        self.type_combobox.addItems(['Todos', 'Personajes', 'Elementos'])

        # al cambiar el texto del combobox se actualiza el layout de los botones segun categoria
        # como al redefinir botones se crean sin su cantidad, envio una señal al backend
        # para que actualice la cantidad disponible de cada entidad
        self.type_combobox.currentTextChanged.connect(self.actualizar_layout_botones)
        self.type_combobox.currentTextChanged.connect(self.enviar_senal_actualizar_cant)

        # creo botones de inicio y salida
        self.boton_inicio = QPushButton('&Iniciar', self)
        self.boton_inicio.clicked.connect(self.inicio_clicked)

        self.boton_limpiar = QPushButton('&Limpiar', self)
        self.boton_limpiar.clicked.connect(self.enviar_orden_limpiar)

        # creo el layout de la mitad izquierda
        self.left_vlayout = QVBoxLayout()

        # le agrego el combo box
        self.left_vlayout.addWidget(self.type_combobox)

        # instancio y agrego botones correspondientes
        botones = self.instanciar_botones(self.type_combobox.currentText())
        for boton in botones:
            self.left_vlayout.addWidget(boton)
        self.left_vlayout.addStretch(1)

        # agrego botones de entrada y salida
        self.left_vlayout.addWidget(self.boton_inicio)
        self.left_vlayout.addWidget(self.boton_limpiar)

        # creo layout global
        placeholder = QGridLayout()
        self.layout_global = QHBoxLayout()
        self.layout_global.addLayout(self.left_vlayout)
        self.layout_global.addLayout(placeholder)  # el gridlayout es un placeholder
        self.setLayout(self.layout_global)

    def instanciar_botones(self, tipo):
        '''
        instancio los botones necesarios para el selector de entidades,
        junto a sus distintos iconos, los almaceno en su dict original
        '''
        # creo botones
        # para entender mejor como se llama cada boton los creo a mano y no ocupo for loop
        self.bot_luigi = BotonArrastable('L', self)
        self.bot_luigi.setIcon(QIcon(p.RUTA_LUIGI))
        self.bot_vghost = BotonArrastable('V', self)
        self.bot_vghost.setIcon(QIcon(p.RUTA_FANTASMA_VERTICAL))
        self.bot_hghost = BotonArrastable('H', self)
        self.bot_hghost.setIcon(QIcon(p.RUTA_FANTASMA_HORIZONTAL))
        self.bot_fire = BotonArrastable('F', self)
        self.bot_fire.setIcon(QIcon(p.RUTA_FIRE))
        self.bot_wall = BotonArrastable('P', self)
        self.bot_wall.setIcon(QIcon(p.RUTA_WALL))
        self.bot_rock = BotonArrastable('R', self)
        self.bot_rock.setIcon(QIcon(p.RUTA_ROCK))
        self.bot_star = BotonArrastable('S', self)
        self.bot_star.setIcon(QIcon(p.RUTA_STAR))

        # creo un dict que los contenga segun tipo:
        self.bot_type = dict()
        self.bot_type['Personajes'] = [self.bot_vghost, self.bot_hghost, self.bot_luigi]
        self.bot_type['Elementos'] = [self.bot_fire, self.bot_rock, self.bot_wall, self.bot_star]
        self.bot_type['Todos'] = self.bot_type['Personajes'] + self.bot_type['Elementos']

        return self.bot_type[tipo]

    def actualizar_layout_botones(self):
        '''
        determina la nueva categoria elegida, elimina todos los widgets del layout
        instancia nuevos botones y los setea en el layout nuevo junto con sus conexiones
        '''
        # defino nueva categoria
        nueva_categoria = self.type_combobox.currentText()

        # creo y conecto nuevos botones de inicio y de salida
        nuevo_boton_inicio = QPushButton('&Iniciar', self)
        nuevo_boton_inicio.clicked.connect(self.inicio_clicked)  # PLACEHOLDER CAMBIAR

        nuevo_boton_limpiar = QPushButton('&Limpiar', self)
        nuevo_boton_limpiar.clicked.connect(self.enviar_orden_limpiar)

        # limpio el layout actual
        while self.left_vlayout.count() > 1:
            item = self.left_vlayout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
            del item

        # instancio nuevos botones, agrego todo al layout
        nuevos_botones = self.instanciar_botones(nueva_categoria)

        for boton in nuevos_botones:
            self.left_vlayout.addWidget(boton)
        self.left_vlayout.addStretch(1)
        self.left_vlayout.addWidget(nuevo_boton_inicio)
        self.left_vlayout.addWidget(nuevo_boton_limpiar)

    def receive_set_grilla(self, grilla):
        for _ in range(1):
            item = self.layout_global.takeAt(1)
            layout_delete = item.layout()
            layout_delete.deleteLater()
        new_grilla = QGridLayout()
        for row in range(len(grilla)):
            for col in range(len(grilla[0])):
                label = QLabel('', self)
                label.setFixedSize(32, 32)
                label.setStyleSheet('background-color: black; border: 1px solid gray')
                label.setAcceptDrops(True)

                # perdon por estas lineas querido ayudante
                if grilla[row][col] == 'B':
                    label.setPixmap(QPixmap(p.PATH_BORDE))
                    label.setStyleSheet('')

                if grilla[row][col] == 'L':
                    label.setPixmap(QPixmap(p.RUTA_LUIGI))

                if grilla[row][col] == 'P':
                    label.setPixmap(QPixmap(p.RUTA_WALL))
                    label.setStyleSheet('')

                if grilla[row][col] == 'F':
                    label.setPixmap(QPixmap(p.RUTA_FIRE))

                if grilla[row][col] == 'R':
                    label.setPixmap(QPixmap(p.RUTA_ROCK))

                if grilla[row][col] == 'H':
                    label.setPixmap(QPixmap(p.RUTA_FANTASMA_HORIZONTAL))

                if grilla[row][col] == 'V':
                    label.setPixmap(QPixmap(p.RUTA_FANTASMA_VERTICAL))

                if grilla[row][col] == 'S':
                    label.setPixmap(QPixmap(p.RUTA_STAR))
                    label.setScaledContents(True)

                new_grilla.addWidget(label, row, col)
        new_grilla.setSpacing(0)
        self.layout_global.addLayout(new_grilla)

    def actualizar_cant_botones(self, class_dict):
        '''recibe un dict con las entidades disponibles en listas separadas por tipo
        determina las nuevas cantidades y se las setea al texto del boton correspondiente'''
        botones = self.bot_type['Todos']
        for boton in botones:
            for boton_id in class_dict.keys():
                if boton_id in boton.text():
                    boton.setText(f'{boton_id} {len(class_dict[boton_id])}')

    def enviar_senal_actualizar_cant(self):
        '''
        utilizado cuando el combobox cambia la categoria de los items visualizados
        le envia una señal al backend para que envia una señal devuelta que
        actualice las cantidades y las setee en botones
        '''
        self.senal_actualizar_cantidad.emit()

    def item_seteado_grilla(self, boton_id, coord):
        '''
        envia el id y las coordenadas del boton cuando una entidad
        es soltada dentro de la grilla al backend,
        este procesa y devuelve la info nueva
        '''
        self.senal_boton_seteado.emit(boton_id, coord)

    def enviar_orden_limpiar(self):
        '''conectado al boton limpiar, emite la señal 'senal_limpiar_grilla'
        que es recibida por el backend y limpia la grilla'''
        self.senal_limpiar_grilla.emit()

    def abrir_ventana_error(self):
        '''abre la ventana de error cuando la posicion de la entidad
        es invalida'''
        self.ventana = VentanaErrorPosicion()
        self.ventana.show()

    def inicio_clicked(self):
        if '0' in self.bot_luigi.text() and '0' in self.bot_star.text():
            self.senal_iniciar_juego.emit()
        else:
            self.ventana = VentanaFaltaLuigi()
            self.ventana.show()

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()
        boton_id = widget.text().split(' ')[0]
        receiving = self.childAt(pos)
        grid_lay = self.layout_global.itemAt(1).layout()

        if receiving is not None and type(receiving) != QPushButton:
            if type(receiving) != QComboBox and type(receiving) != BotonArrastable:
                coords = grid_lay.getItemPosition(grid_lay.indexOf(receiving))[:2]
                self.item_seteado_grilla(boton_id, coords)
        e.ignore()
        widget.repaint()
