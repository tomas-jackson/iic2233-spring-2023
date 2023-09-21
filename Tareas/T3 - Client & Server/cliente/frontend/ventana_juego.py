from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, QApplication
from PyQt5.QtWidgets import QComboBox
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys
from os.path import join
import json
from collections import namedtuple


class VentanaJuego(QWidget):

    senal_orden_reroll = pyqtSignal(list)
    senal_enviar_num = pyqtSignal(list)
    senal_paso = pyqtSignal(list)
    senal_dudar = pyqtSignal(list)
    senal_boton_poder = pyqtSignal(list)
    senal_poder_target = pyqtSignal(list)
    senal_cerrar_socket = pyqtSignal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.showing = False
        self.dc = False
        self.con_error = False
        self.paths = self.cargar_dict()
        self.sprites = self.dict_sprites()
        self.init_gui()

    def init_gui(self):
        uic.loadUi(join('cliente', 'frontend', 'ui', 'ventana_juego.ui'), self)

        self.label_pfp1 = self.findChild(QLabel, 'label_pfp1')
        self.label_pfp2 = self.findChild(QLabel, 'label_pfp2')
        self.label_pfp3 = self.findChild(QLabel, 'label_pfp3')
        self.label_pfp4 = self.findChild(QLabel, 'label_pfp4')

        self.pfps = [self.label_pfp1, self.label_pfp2, self.label_pfp3, self.label_pfp4]

        for pfp in self.pfps:
            pfp.setPixmap(self.sprites['avatar'])

        self.dado1_1 = self.findChild(QLabel, 'dado1_1')
        self.dado1_2 = self.findChild(QLabel, 'dado1_2')
        self.dado2_1 = self.findChild(QLabel, 'dado2_1')
        self.dado2_2 = self.findChild(QLabel, 'dado2_2')
        self.dado3_1 = self.findChild(QLabel, 'dado3_1')
        self.dado3_2 = self.findChild(QLabel, 'dado3_2')
        self.dado4_1 = self.findChild(QLabel, 'dado4_1')
        self.dado4_2 = self.findChild(QLabel, 'dado4_2')

        self.dados = [self.dado1_1, self.dado1_2, self.dado2_1, self.dado2_2,
                      self.dado3_1, self.dado3_2, self.dado4_1, self.dado4_2]

        self.label_id1 = self.findChild(QLabel, 'label_id1')
        self.label_id2 = self.findChild(QLabel, 'label_id2')
        self.label_id3 = self.findChild(QLabel, 'label_id3')
        self.label_id4 = self.findChild(QLabel, 'label_id4')

        self.ids = [self.label_id1, self.label_id2, self.label_id3, self.label_id4]
        for id_ in self.ids:
            id_.resize(id_.sizeHint())

        self.label_vida1 = self.findChild(QLabel, 'label_vida1')
        self.label_vida2 = self.findChild(QLabel, 'label_vida2')
        self.label_vida3 = self.findChild(QLabel, 'label_vida3')
        self.label_vida4 = self.findChild(QLabel, 'label_vida4')

        self.vidas = [self.label_vida1, self.label_vida2, self.label_vida3, self.label_vida4]

        self.label_mayor_num = self.findChild(QLabel, 'label_mayor_num')
        self.label_id_actual = self.findChild(QLabel, 'label_id_actual')
        self.label_id_pasado = self.findChild(QLabel, 'label_id_pasado')
        self.label_turno = self.findChild(QLabel, 'label_turno')

        self.boton_enviar = self.findChild(QPushButton, 'boton_enviar')
        self.boton_pasar = self.findChild(QPushButton, 'boton_pasar')
        self.boton_reroll = self.findChild(QPushButton, 'boton_reroll')
        self.boton_poder = self.findChild(QPushButton, 'boton_poder')
        self.boton_dudar = self.findChild(QPushButton, 'boton_dudar')
        self.edit_valor = self.findChild(QLineEdit, 'edit_valor')

        self.boton_reroll.clicked.connect(self.enviar_reroll)
        self.boton_enviar.clicked.connect(self.enviar_num)
        self.boton_pasar.clicked.connect(lambda x: self.senal_paso.emit(['PASS']))
        self.boton_dudar.clicked.connect(lambda x: self.senal_dudar.emit(['DUDAR']))
        self.boton_poder.clicked.connect(lambda x: self.senal_boton_poder.emit(['CHECK PODER']))

        self.label_background = self.findChild(QLabel, 'label_background')
        self.label_background.setPixmap(self.sprites['fondo'])

        self.player_info = namedtuple('id', ['dado1', 'dado2', 'vidas', 'nombre'])

        self.posiciones = {
            'id1': self.player_info(self.dado1_1, self.dado1_2, self.label_vida1, self.label_id1),
            'id2': self.player_info(self.dado2_1, self.dado2_2, self.label_vida2, self.label_id2),
            'id3': self.player_info(self.dado3_1, self.dado3_2, self.label_vida3, self.label_id3),
            'id4': self.player_info(self.dado4_1, self.dado4_2, self.label_vida4, self.label_id4),
        }

        self.combo_targets = QComboBox(self)
        self.boton_ataque = QPushButton('ATACAR!', self)
        self.boton_ataque.clicked.connect(self.enviar_target)
        self.combo_targets.move(490, 300)
        self.boton_ataque.move(400, 300)
        self.combo_targets.hide()
        self.boton_ataque.hide()

    def cargar_dict(self):
        with open(join('cliente', 'parametros.json')) as file:
            dicc = json.load(file)
        return dicc

    def dict_sprites(self) -> dict:
        '''
        crea y retorna un diccionario que incluye a los pixmaps de todos los sprites
        a usar
        '''
        diccionario = {
            'dado1': QPixmap(join(*self.paths['dado1'])),
            'dado2': QPixmap(join(*self.paths['dado2'])),
            'dado3': QPixmap(join(*self.paths['dado3'])),
            'dado4': QPixmap(join(*self.paths['dado4'])),
            'dado5': QPixmap(join(*self.paths['dado5'])),
            'dado6': QPixmap(join(*self.paths['dado6'])),
            'avatar': QPixmap(join(*self.paths['avatar'])),
            'fondo': QPixmap(join(*self.paths['fondo_juego']))
        }
        return diccionario

    def recibir_info_round(self, dic_personal: dict, lista_dic: list) -> None:
        '''
        recibe un diccionario con la info personal del cliente y la muestra en ventana
        '''

        numero_id = dic_personal['pos']

        self.posiciones[numero_id].dado1.setPixmap(self.sprites[dic_personal['dados'][0]])
        self.posiciones[numero_id].dado2.setPixmap(self.sprites[dic_personal['dados'][1]])
        self.posiciones[numero_id].vidas.setText(f'Vidas: {dic_personal["vidas"]}')
        self.posiciones[numero_id].vidas.resize(self.posiciones[numero_id].vidas.sizeHint())
        self.posiciones[numero_id].nombre.setText(dic_personal['id'])

        for dic_general in lista_dic:
            pos = dic_general['pos']
            self.posiciones[pos].vidas.setText(f'Vidas: {dic_general["vidas"]}')
            self.posiciones[pos].nombre.setText(dic_general['id'])
            self.posiciones[pos].dado1.clear()
            self.posiciones[pos].dado2.clear()

    def habilitar_botones(self):
        self.boton_dudar.setEnabled(True)
        self.boton_enviar.setEnabled(True)
        self.boton_pasar.setEnabled(True)
        self.boton_poder.setEnabled(True)
        self.boton_reroll.setEnabled(True)
        self.edit_valor.setEnabled(True)

    def inhabilitar_botones(self):
        self.boton_dudar.setEnabled(False)
        self.boton_enviar.setEnabled(False)
        self.boton_pasar.setEnabled(False)
        self.boton_poder.setEnabled(False)
        self.boton_reroll.setEnabled(False)
        self.edit_valor.setEnabled(False)

    def cambiar_actual(self, nombre: str) -> None:
        self.label_id_actual.setText(f'Turno actual: {nombre}')
        self.label_id_actual.resize(self.label_id_actual.sizeHint())

    def enviar_reroll(self):
        self.senal_orden_reroll.emit(['REROLL'])
        self.boton_reroll.setEnabled(False)
        self.boton_dudar.setEnabled(False)

    def enviar_num(self):
        self.senal_enviar_num.emit(['NUMBER', self.edit_valor.text()])

    def cambiar_dados(self, dados_pos: list) -> None:
        dado1 = dados_pos[0][0]
        dado2 = dados_pos[0][1]
        pos = dados_pos[1]
        self.posiciones[pos].dado1.setPixmap(self.sprites[dado1])
        self.posiciones[pos].dado2.setPixmap(self.sprites[dado2])

    def handle_num_respuesta(self, info):
        razon = info[0]
        self.edit_valor.clear()
        if razon == 'NONDIGIT':
            self.edit_valor.setPlaceholderText(' Debes ingresar un numero valido')
            self.edit_valor.setToolTip('Debes ingresar un numero valido')
        if razon == 'LOWER':
            self.edit_valor.setPlaceholderText(' Numero debe ser mayor al maximo anunciado')
            self.edit_valor.setToolTip('Numero debe ser mayor al maximo anunciado')
        if razon == 'NUM VALIDO':
            self.edit_valor.setPlaceholderText(' Ingresar valor aqui')
            self.edit_valor.setToolTip('')
            self.label_mayor_num.setText(f'Mayor numero: {info[1]}')
            self.label_mayor_num.resize(self.label_mayor_num.sizeHint())

    def update_banner(self, info):
        new_name = info[0]
        old_name = info[1]
        turno_actual = info[2]
        self.label_id_actual.setText(f'Turno actual: {new_name}')
        self.label_id_actual.resize(self.label_id_actual.sizeHint())
        self.label_id_pasado.setText(f'Turno pasado: {old_name}')
        self.label_id_pasado.resize(self.label_id_pasado.sizeHint())
        self.label_turno.setText(f'Numero de turno: {turno_actual}')
        self.label_turno.resize(self.label_turno.sizeHint())

    def mostrar_dados(self, info):
        self.inhabilitar_botones()
        for data in info:
            pos = data['pos']
            self.posiciones[pos].dado1.setPixmap(self.sprites[data['dados'][0]])
            self.posiciones[pos].dado2.setPixmap(self.sprites[data['dados'][1]])

    def mostrar_popup_muerte(self):
        if self.dc is False:
            self.showing = True
            QMessageBox.information(self, 'Muerte', 'Te quedaste sin vidas - Desconectando')
            self.close()

    def abrir_popup_ganar(self):
        self.showing = True
        QMessageBox.information(self, 'VICTORIA', 'FELICITACIONES - GANASTE')
        self.close()

    def popup_dead_server(self):
        if self.isVisible() is True and self.showing is False:
            self.showing = True
            QMessageBox.information(self, 'Desconectado', 'El servidor se desconecto - Saliendo')
            self.close()

    def popup_no_poder(self):
        QMessageBox.information(self, 'Sin dados', 'No tienes los dados para usar un poder')

    def mostrar_no_duda(self):
        QMessageBox.information(self, 'No se puede dudar',
                                'No hay ninguna accion que puedas dudar')

    def mostrar_combo(self, nombres):
        self.combo_targets.addItems(nombres)
        self.combo_targets.show()
        self.boton_ataque.show()

    def enviar_target(self):
        target = self.combo_targets.currentText()
        self.senal_poder_target.emit(['OBJETIVO', target])
        self.combo_targets.hide()
        self.combo_targets.clear()
        self.boton_ataque.hide()
        self.inhabilitar_botones()

    def closeEvent(self, e):
        self.dc = True
        if self.showing is False:
            self.senal_cerrar_socket.emit()


if __name__ == '__main__':
    app = QApplication([])
    instanciador = VentanaJuego()
    instanciador.show()
    sys.exit(app.exec_())
