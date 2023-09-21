import random as r
from time import sleep
from collections import deque
import socket


class Bot():

    def __init__(self, prob_dudar, prob_anunciar, valor_paso, name, pos, vidas) -> None:
        self.prob_dudar = prob_dudar
        self.prob_anunciar = prob_anunciar
        self.valor_paso = valor_paso
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id = name
        self.pos = pos
        self._vidas = vidas
        self.muerto = False
        self._mintiendo = False
        self.dados = r.choices(['dado1', 'dado2', 'dado3', 'dado4', 'dado5', 'dado6'], k=2)
        self.suma = int(self.dados[0][4]) + int(self.dados[1][4])
        self.dict = {
                'id': self.id,
                'pos': self.pos,
                'vidas': self.vidas,
                'mintiendo': self.mintiendo,
                'dados': self.dados,
                'suma': self.suma,
                'address': 'BOT'
        }

    @property
    def vidas(self):
        return self._vidas

    @vidas.setter
    def vidas(self, n):
        if n <= 0:
            self.muerto = True
            self._vidas = 0
        else:
            self._vidas = n
        self.dict['vidas'] = self.vidas

    @property
    def mintiendo(self):
        return self._mintiendo

    @mintiendo.setter
    def mintiendo(self, n: bool):
        self._mintiendo = n
        self.dict['mintiendo'] = n

    def reroll(self):
        self.dados = r.choices(['dado1', 'dado2', 'dado3', 'dado4', 'dado5', 'dado6'], k=2)
        self.suma = self.suma = int(self.dados[0][4]) + int(self.dados[1][4])
        self.dict['dados'] = self.dados
        self.dict['suma'] = self.suma

    def anunciar(self, anterior):
        valor = r.randint(anterior + 1, 12)
        if valor != self.suma:
            self.mintiendo = True
        return ['NUMBER', str(valor)]

    def dudar(self):
        return True

    def pasar(self):
        if self.suma != self.valor_paso:
            self.mintiendo = True

    def damage(self):
        self.vidas -= 1

    def jugar_turno(self, anterior, turno_actual):
        print(f'[LOG] {self.id} (bot) pensando')
        sleep(3)
        if self.muerto is True:
            return 'muerto'
        else:
            opcion1 = ['dudar', 'reroll']
            pesos1 = [self.prob_dudar, 1 - self.prob_dudar]
            eleccion = r.choices(opcion1, pesos1, k=1)
            if eleccion[0] == 'dudar' and turno_actual != 1:
                return ['DUDAR']
            else:
                self.reroll()
                opcion2 = ['anunciar', 'pasar']
                pesos2 = [self.prob_anunciar, 1 - self.prob_anunciar]
                eleccion2 = r.choices(opcion2, pesos2, k=1)
                if eleccion2[0] == 'anunciar' and anterior != 12:
                    respuesta = self.anunciar(anterior)
                    return respuesta
                else:
                    self.pasar()
                    return ['PASS']


def choose_next_pos(pos: str, dic: dict) -> str:
    disp = [dic[skt]['pos'] for skt in dic.keys()]
    disp.sort()
    indice = disp.index(pos)
    new_pos = disp[indice - 1]
    return new_pos


def choose_bot(sock, bot_list):
    for bot in bot_list:
        if sock == bot.sock:
            return bot


def clear_queue(queue, func):
    '''
    libera a toda la gente en cola, envia un mensaje a su socket avisando
    '''
    for sock in queue:
        func(['ingame'], sock[0])
        sock[0].close()
    queue = deque([])


def check_dados(key, dic):
    set1 = {'dado1', 'dado2'}
    set2 = {'dado1', 'dado3'}
    if set(dic[key]['dados']) in [set1, set2]:
        return ['SI PODER']
    else:
        return ['NO PODER']


def find_sock(name: str, dic: dict):
    for key in dic.keys():
        if name == dic[key]['id']:
            return key
