import socket
import threading
import json
from os.path import join
from Scripts import cripto as c
from collections import deque
from time import sleep
import random as r
import utility as f
import sys


class Servidor():

    def __init__(self, port):

        self.lock = threading.Lock()
        self.max_recv = 2**16
        self.parametros = self.net_info()
        self.host = self.parametros['host']
        self.port = port
        self.clientes_maximos = self.parametros['NUMERO_JUGADORES']
        self.player_pos = ['id1', 'id2', 'id3', 'id4']
        self.ingame = False
        self.jugador_actual = None  # cuando se asigne va a ser el socket representandolo
        self.jugador_pasado = None
        self.ganador = None
        self.numero_maximo = 0
        self.turno_actual = 1
        self.lista_espera = deque([])
        self.id_disponibles = self.lista_id()
        self.id_usados = []
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets = {}
        self.conectado = True
        self.bindear_conectar()
        self.aceptar_conexiones()
        self.bots = []
        self.bot_socks = []

    def interpretar_msg(self, mensaje, socket_cliente) -> None:
        if mensaje[0] == 'START':
            self.instanciar_bots()
            f.clear_queue(self.lista_espera, self.enviar)
            print(f'[LOG] Comenzando el juego con: {", ".join(self.id_usados)}')
            # envio info de la ronda inicial
            self.enviar_info_ronda()

        if mensaje[0] == 'CHECK PODER':
            respuesta = f.check_dados(socket_cliente, self.sockets)
            self.enviar(respuesta + self.id_usados, socket_cliente)

        if mensaje[0] == 'OBJETIVO':
            print(f'[LOG] {self.sockets[socket_cliente]["id"]} usa poder contra {mensaje[1]}')
            self.handle_poder(socket_cliente, mensaje[1])

        if mensaje[0] == 'DUDAR':
            print(f'[LOG] {self.sockets[socket_cliente]["id"]} decide dudar')
            self.handle_dudar()

        if mensaje[0] == 'NUMBER':
            can_send = self.handle_number(mensaje[1], socket_cliente)
            print(f'[LOG] {self.sockets[socket_cliente]["id"]} anuncia un {mensaje[1]}')
            if can_send is True:
                sleep(0.1)
                self.next_turn()

        if mensaje[0] == 'REROLL':
            print(f'[LOG] {self.sockets[socket_cliente]["id"]} decide cambiar dados')
            self.handle_reroll(socket_cliente)

        if mensaje[0] == 'PASS':
            print(f'[LOG] {self.sockets[socket_cliente]["id"]} decide pasar')
            if self.sockets[socket_cliente]['suma'] != self.parametros['VALOR_PASO']:
                self.sockets[socket_cliente]['mintiendo'] = True
            self.next_turn()

        if mensaje[0] == 'cerrado':
            self.sockets[socket_cliente]['vidas'] = 0
            self.jugador_actual = socket_cliente
            self.jugador_pasado = None
            self.enviar_info_ronda()

    def net_info(self) -> dict:
        with open(join('servidor', 'parametros.json'), 'r', encoding='UTF-8') as file:
            parametros = json.load(file)
        return parametros

    def lista_id(self) -> list:
        lista = [self.parametros[key] for key in self.parametros.keys() if 'id_' in key]
        return lista

    def bindear_conectar(self):
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        print(f'El servidor esta escuchando en {self.host}:{self.port}')

    def aceptar_conexiones(self):
        thread = threading.Thread(target=self.thread_aceptar_conexiones)
        thread.start()

    def thread_aceptar_conexiones(self):
        while self.conectado:
            try:
                socket_cliente, address = self.socket_server.accept()
                self.handle_connection(socket_cliente, address)
            except ConnectionAbortedError:
                print('[LOG] Cerrando server')

    def thread_manejar_requests(self, socket_cliente):
        while self.conectado:
            try:
                # determino la longitud del mensaje original
                length_data = socket_cliente.recv(4)
                largo_archivo = int.from_bytes(
                    length_data, byteorder='little')
                # adapto la longitud al mensaje encriptado
                largo_archivo += (128 - (largo_archivo % 128))
                largo_archivo += (largo_archivo // 128) * 4
                length_data = bytearray(length_data)
                if largo_archivo > self.max_recv:
                    largo_archivo = self.max_recv
                bytes_leidos = bytearray()
                # leo los bytes del archivo
                while len(bytes_leidos) < largo_archivo:
                    bytes_leer = min(4096, largo_archivo - len(bytes_leidos))
                    respuesta = socket_cliente.recv(bytes_leer)
                    bytes_leidos += respuesta
                bytes_finales = length_data + bytes_leidos
                recuperado = c.recuperar_mensaje(bytes_finales, self.parametros['N_PONDERADOR'])
                mensaje_final = json.loads(recuperado.decode('utf-8'))
                # si el mensaje es igual a dc, significa que el cliente se desconecta
                # inmediatamente despues de mandarlo, por lo que lo desconecto
                # y libero su socket e id
                if mensaje_final[0] == 'dc':
                    raise ConnectionError
                else:
                    self.interpretar_msg(mensaje_final, socket_cliente)
            except (ConnectionError, OSError):
                if socket_cliente in self.sockets.keys():
                    self.handle_dc(socket_cliente)
                break

    def enviar(self, mensaje, socket_cliente) -> None:
        if socket_cliente not in self.bot_socks:
            with self.lock:
                bitificado = json.dumps(mensaje).encode('utf-8')
                data = c.procesar_mensaje(bitificado, self.parametros['N_PONDERADOR'])
                socket_cliente.sendall(data)

    def actualizacion_usuarios(self):
        '''
        manda el cambio en usuarios usados al cliente
        '''
        sleep(0.1)
        # pongo este delay para asegurar que la conexion entre cliente y front end ocurra antes
        mensaje = "Usuarios-"+'-'.join(self.id_usados)
        for sock in self.sockets.keys():
            self.enviar([mensaje], sock)

    def conectar_cola(self, client_data):
        '''
        conecta al cliente entregado al juego principal, analogo
        de thread_aceptar_conexiones
        '''
        new_client_socket = client_data[0]
        self.enviar(['Spot Open'], new_client_socket)
        address = client_data[1]
        self.handle_connection(new_client_socket, address)

    def handle_connection(self, socket_cliente, address):
        if len(self.sockets) < self.clientes_maximos and self.ingame is False:
            id_cliente = self.id_disponibles.pop()
            pos_cliente = self.player_pos.pop(0)
            self.id_usados.append(id_cliente)
            self.sockets[socket_cliente] = {
                'address': address,
                'id': id_cliente,
                'pos': pos_cliente,
                'vidas': self.parametros['NUMERO_VIDAS'],
                'mintiendo': False
                }
            msg_1 = self.sockets[socket_cliente]["id"]
            msg_2 = self.sockets[socket_cliente]["address"]
            print(f'[LOG] {msg_2} conectado como {msg_1}')
            thread_requests = threading.Thread(
                target=self.thread_manejar_requests,
                args=(socket_cliente, ),
                daemon=True)
            self.actualizacion_usuarios()
            thread_requests.start()
        # si es que no hay espacio pero todavia no parte
        elif len(self.sockets) == self.clientes_maximos and self.ingame is False:
            self.lista_espera.append((socket_cliente, address))
            sleep(0.1)  # dar tiempo para hacer conexiones
            self.enviar(['Party Full'], socket_cliente)
        # si es que la partida ya inicio
        elif self.ingame is True:
            sleep(0.1)  # dar tiempo para terminar conexiones
            self.enviar(['ingame'], socket_cliente)
            socket_cliente.close()

    def handle_dc(self, socket_cliente: socket.socket) -> None:
        '''
        libera los recursos utilizados por el cliente que se acaba de desconectar
        '''
        name = self.sockets[socket_cliente]["id"]
        add = self.sockets[socket_cliente]['address']
        print(f'[LOG] {name} {add} desconectado')
        self.id_usados.remove(self.sockets[socket_cliente]["id"])
        self.id_disponibles.append(self.sockets[socket_cliente]["id"])
        self.player_pos.append(self.sockets[socket_cliente]['pos'])
        self.sockets.pop(socket_cliente)
        if socket_cliente not in self.bot_socks:
            self.actualizacion_usuarios()
            if len(self.lista_espera) > 0:
                # NO HAY MANEJO SI UN SOCKET EN COLA SE DESCONECTA
                # NO LO VOY A HACER HASTA QUE TERMINE EL RESTO, VA AL README
                # AYUDANTE SI LEES ESTO ES PORQUE NO LO HICE,
                # POR FAVOR NO DESCONECTES UN CLIENTE EN COLA T.T
                new_client = self.lista_espera.popleft()
                self.conectar_cola(new_client)
            socket_cliente.close()

    def enviar_info_ronda(self, data_dead=None, dc=False):
        # si es que es la primera ronda elige un actual al azar
        if self.ingame is False:
            self.jugador_actual = r.choice(list(self.sockets.keys()))
            self.ingame = True
        # si el actual esta muerto hace handling del caso
        if self.sockets[self.jugador_actual]['vidas'] <= 0:
            data_dead = [self.sockets[self.jugador_actual]]
            self.handle_muerte(self.jugador_actual)
        # le envia la info necesaria a todos los clientes
        for sock in self.sockets.keys():
            dados = r.choices(['dado1', 'dado2', 'dado3', 'dado4', 'dado5', 'dado6'], k=2)
            self.sockets[sock]['dados'] = dados
            self.sockets[sock]['suma'] = int(dados[0][4]) + int(dados[1][4])
            self.sockets[sock]['mintiendo'] = False
            con_data = list(self.sockets.values())
            info_general = con_data + data_dead if data_dead is not None else con_data
            info_general.remove(self.sockets[sock])
            info_jugador_actual = self.sockets[self.jugador_actual]
            past = self.jugador_pasado
            name_pasado = self.sockets[past]['id'] if past is not None else 'n/a'
            self.enviar(
                ['start round', self.sockets[sock], info_general, info_jugador_actual], sock)
            sleep(0.01)
            info = ['INFO BANNER', info_jugador_actual['id'], name_pasado, self.turno_actual]
            self.enviar(info, sock)
            sleep(0.01)
            self.enviar(['NUM VALIDO', 0], sock)
        print(f'[LOG] Comienza el turno de: {self.sockets[self.jugador_actual]["id"]}')
        # checkeo si hay un ganador
        if self.check_win() is True:
            self.enviar(['GANASTE'], self.ganador)
            print(f'[LOG] {self.sockets[self.ganador]["id"]} es el ganador!!!')
            print('[LOG] Terminando partida')
            self.handle_dc(self.ganador)
            self.conectado = False
            self.socket_server.close()

        if self.jugador_actual in self.bot_socks:
            bot = f.choose_bot(self.jugador_actual, self.bots)
            self.play_bot(bot)

    def handle_reroll(self, sock):
        new_dados = r.choices(['dado1', 'dado2', 'dado3', 'dado4', 'dado5', 'dado6'], k=2)
        self.sockets[sock]['dados'] = new_dados
        self.sockets[sock]['suma'] = int(new_dados[0][4]) + int(new_dados[1][4])
        pos_cliente = self.sockets[sock]['pos']
        self.enviar(['REROLL', new_dados, pos_cliente], sock)

    def handle_number(self, num: str, sock: socket.socket) -> bool:
        if num.isdigit() is False or int(num) > 12:
            self.enviar(['NONDIGIT'], sock)
            return False
        elif int(num) <= self.numero_maximo:
            self.enviar(['LOWER'], sock)
            return False
        else:
            self.numero_maximo = int(num)
            for skt in self.sockets.keys():
                self.enviar(['NUM VALIDO', num], skt)

            if int(num) != self.sockets[sock]['suma']:
                self.sockets[sock]['mintiendo'] = True
        return True

    def next_turn(self):
        if self.jugador_pasado is not None:
            self.sockets[self.jugador_pasado]['mintiendo'] = False
        self.jugador_pasado = self.jugador_actual
        self.turno_actual += 1
        pos_actual = self.sockets[self.jugador_actual]['pos']
        new_pos = f.choose_next_pos(pos_actual, self.sockets)
        for skt in self.sockets.keys():
            if self.sockets[skt]['pos'] == new_pos:
                self.jugador_actual = skt
        nombre_nuevo = self.sockets[self.jugador_actual]['id']
        nombre_viejo = self.sockets[self.jugador_pasado]['id']
        for skt in self.sockets.keys():
            sleep(0.01)
            self.enviar(['INFO BANNER', nombre_nuevo, nombre_viejo, self.turno_actual], skt)
            sleep(0.01)
        sleep(0.01)
        self.enviar(['HABILITAR'], self.jugador_actual)
        sleep(0.01)
        self.enviar(['INHABILITAR'], self.jugador_pasado)
        print(f'[LOG] Comienza el turno de: {nombre_nuevo}')
        if self.jugador_actual in self.bot_socks:
            bot = f.choose_bot(self.jugador_actual, self.bots)
            self.play_bot(bot)

    def handle_dudar(self):
        # checkeo los dos casos posibles, segun eso defino cual es el nuevo jugador actual
        if self.turno_actual > 1:
            if self.sockets[self.jugador_pasado]['mintiendo'] is True:
                self.sockets[self.jugador_pasado]['vidas'] -= 1
                self.jugador_actual = self.jugador_pasado
                self.jugador_pasado = None
            elif self.sockets[self.jugador_pasado]['mintiendo'] is False:
                self.sockets[self.jugador_actual]['vidas'] -= 1
                self.jugador_pasado = None
            self.turno_actual = 1
            self.numero_maximo = 0
            nombre_nuevo = self.sockets[self.jugador_actual]['id']
            vidas = self.sockets[self.jugador_actual]["vidas"]
            print(f'[LOG] Le quedan {vidas} vidas a {nombre_nuevo}')
            for skt in self.sockets.keys():
                sleep(0.01)
                self.enviar(['MOSTRAR DADOS', list(self.sockets.values())], skt)
            sleep(5)
            # el checkeo de si esta muerto el actual ocurre en el metodo de abajo
            self.enviar_info_ronda()
        else:
            self.enviar(['NO DUDA'], self.jugador_actual)

    def handle_muerte(self, sock):
        new_pos = f.choose_next_pos(self.sockets[sock]['pos'], self.sockets)
        for skt in self.sockets.keys():
            if self.sockets[skt]['pos'] == new_pos:
                self.jugador_actual = skt
        self.enviar(['SKILL ISSUE'], sock)
        self.handle_dc(sock)

    def check_win(self):
        if len(self.sockets.keys()) == 1:
            self.ganador = list(self.sockets.keys())[0]
            return True

    def instanciar_bots(self):
        for i in range(self.parametros['NUMERO_JUGADORES'] - len(self.sockets.keys())):
            bot_id = self.id_disponibles.pop(0)
            self.id_usados.append(bot_id)
            bot_pos = self.player_pos.pop(0)
            bot = f.Bot(self.parametros['PROB_DUDAR'], self.parametros['PROB_ANUNCIAR'],
                        self.parametros['VALOR_PASO'], bot_id, bot_pos,
                        self.parametros['NUMERO_VIDAS'])
            self.bots.append(bot)
            self.bot_socks.append(bot.sock)
            self.sockets[bot.sock] = bot.dict

    def play_bot(self, bot: f.Bot):
        mensaje = bot.jugar_turno(self.numero_maximo, self.turno_actual)
        self.interpretar_msg(mensaje, bot.sock)

    def handle_poder(self, socket_cliente: socket.socket, objetivo: str):
        sock_obj = f.find_sock(objetivo, self.sockets)
        if set(self.sockets[socket_cliente]['dados']) == {'dado1', 'dado2'}:
            print('[LOG] Ataque!')
            self.sockets[sock_obj]['vidas'] -= 1
            self.jugador_actual = sock_obj
            self.jugador_pasado = None
        elif set(self.sockets[socket_cliente]['dados']) == {'dado1', 'dado3'}:
            print('[LOG] Terremoto!')
            self.sockets[sock_obj]['vidas'] = r.randint(1, self.parametros['NUMERO_VIDAS'])
            self.jugador_actual = sock_obj
            self.jugador_pasado = None
        for skt in self.sockets.keys():
            self.enviar(['MOSTRAR DADOS', [self.sockets[socket_cliente]]], skt)
        sleep(5)
        self.enviar_info_ronda()


if __name__ == '__main__':
    port = int(sys.argv[1])
    server = Servidor(port)
