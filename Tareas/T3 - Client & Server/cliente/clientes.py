from PyQt5.QtCore import QObject, pyqtSignal
from os.path import join
from Scripts import cripto
import threading
import socket
import json


class Cliente(QObject):

    senal_parametros = pyqtSignal(dict)
    senal_cambiar_usuarios = pyqtSignal(list)
    senal_popup_full = pyqtSignal()
    senal_spot_open = pyqtSignal()
    senal_ingame = pyqtSignal()
    senal_start_round = pyqtSignal(dict, list)
    senal_botones_jugar_si = pyqtSignal()
    senal_botones_jugar_no = pyqtSignal()
    senal_cambiar_actual = pyqtSignal(str)
    senal_reroll = pyqtSignal(list)
    senal_num_respuesta = pyqtSignal(list)
    senal_info_banner = pyqtSignal(list)
    senal_mostrar_dados = pyqtSignal(list)
    senal_popup_muerte = pyqtSignal()
    senal_ganar = pyqtSignal()
    senal_dead_server = pyqtSignal()
    senal_mostrar_combo = pyqtSignal(list)
    senal_no_dados = pyqtSignal()
    senal_no_dudar = pyqtSignal()

    def __init__(self, port, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parametros = self.leer_p()
        self.id = None
        self.host = self.parametros['host']
        self.port = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.conectarse()
            self.conectado = True
            self.escuchar()
        except ConnectionError:
            print('Error de conexion')
            self.conectado = False
            self.socket_cliente.close()

    def leer_p(self) -> dict:
        '''
        lee el archivo parametros.jason, retorna el diccionario
        '''
        with open(join('cliente', 'parametros.json'), 'r', encoding='UTF-8') as file:
            return json.load(file)

    def conectarse(self) -> None:
        '''
        se conecta al servidor entregado
        '''
        self.socket_cliente.connect((self.host, self.port))

    def escuchar(self) -> None:
        '''
        inicia el thread que se encarga de escuchar al servidoy y recibir la
        informacion que envia
        '''
        self.thread = threading.Thread(target=self.thread_escuchar, daemon=True)
        self.thread.start()

    def thread_escuchar(self) -> None:
        '''
        thread que se encarga de recibir y procesar informacion del server
        '''
        while self.conectado is True:
            try:
                data = self.socket_cliente.recv(2**16)
                bytes_recuperados = cripto.recuperar_mensaje(data, self.parametros['N_PONDERADOR'])
                mensaje_final = json.loads(bytes_recuperados.decode('utf-8'))
                self.procesar_mensaje(mensaje_final)
            except (ConnectionResetError, IndexError):
                self.senal_dead_server.emit()
                self.conectado = False
                self.socket_cliente.close()

    def procesar_mensaje(self, mensaje):
        '''
        analiza los contenidos del mensaje y actua segun estos
        '''
        if "Usuarios" in mensaje[0]:
            usuarios = mensaje[0].split('-')[1:]
            while len(usuarios) < 4:
                usuarios.append('Buscando...')
            self.senal_cambiar_usuarios.emit(usuarios)

        if mensaje[0] == 'Party Full':
            self.senal_popup_full.emit()

        if mensaje[0] == 'Spot Open':
            self.senal_spot_open.emit()

        if mensaje[0] == 'ingame':
            self.senal_ingame.emit()

        if mensaje[0] == 'start round':
            # la estructura del mensaje es una lista de la forma
            # ['start round', dict_info_personal, list_info_general, dict_jugador_actual]
            info_personal = mensaje[1]
            info_general = mensaje[2]
            info_jugando = mensaje[3]
            self.senal_start_round.emit(info_personal, info_general)
            self.senal_cambiar_actual.emit(info_jugando['id'])
            self.id = info_personal['pos']
            if self.id == info_jugando['pos']:
                self.senal_botones_jugar_si.emit()
            else:
                self.senal_botones_jugar_no.emit()

        if mensaje[0] == 'REROLL':
            new_dados_pos = mensaje[1:]
            self.senal_reroll.emit(new_dados_pos)

        if mensaje[0] == 'NONDIGIT':
            self.senal_num_respuesta.emit(['NONDIGIT'])

        if mensaje[0] == 'LOWER':
            self.senal_num_respuesta.emit(['LOWER'])

        if mensaje[0] == 'NUM VALIDO':
            self.senal_num_respuesta.emit(mensaje)

        if mensaje[0] == 'HABILITAR':
            self.senal_botones_jugar_si.emit()

        if mensaje[0] == 'INHABILITAR':
            self.senal_botones_jugar_no.emit()

        if mensaje[0] == 'INFO BANNER':
            self.senal_info_banner.emit(mensaje[1:])

        if mensaje[0] == 'MOSTRAR DADOS':
            self.senal_mostrar_dados.emit(mensaje[1])

        if mensaje[0] == 'SKILL ISSUE':
            self.senal_popup_muerte.emit()

        if mensaje[0] == 'GANASTE':
            self.senal_ganar.emit()

        if mensaje[0] == 'SI PODER':
            self.senal_mostrar_combo.emit(mensaje[1:])

        if mensaje[0] == 'NO PODER':
            self.senal_no_dados.emit()

        if mensaje[0] == 'NO DUDA':
            self.senal_no_dudar.emit()

    def enviar_info(self, mensaje) -> None:
        '''
        metodo encargado de enviar informacion al server conectado
        '''
        bitificado = json.dumps(mensaje).encode('utf-8')
        procesado = cripto.procesar_mensaje(bitificado, self.parametros['N_PONDERADOR'])
        self.socket_cliente.sendall(procesado)

    def enviar_diccionario_front(self) -> None:
        self.senal_parametros.emit(self.parametros)

    def cerrar_socket(self):
        self.enviar_info(['cerrado'])
