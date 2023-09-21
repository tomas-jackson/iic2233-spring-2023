'''
aca ocurre el procesamiento de informacion para la ventana de inicio
'''
import os
import parametros
from PyQt5.QtCore import QObject, pyqtSignal


class ProcesadorInicio(QObject):

    senal_info_mapa = pyqtSignal(list)
    senal_start = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extraer_mapas(self):
        '''
        lee los mapas disponibles y mediante la señal 'senal_info_mapa'
        se lo envia al front end, esta señal se conecta al metodo
        actualizar_combobox del frontend
        '''
        mapas = os.listdir(os.path.join('mapas'))
        mapas_sin_ext = [os.path.splitext(x)[0] for x in mapas]
        self.senal_info_mapa.emit(mapas_sin_ext)

    def verificar_informacion(self, datos):
        '''
        recibe, mediante 'senal_inicio', la seleccion de mapa y el user,
        aca procesa si el user es valido y determina el nombre de archivo del mapa
        devuelve la informacion procesada al front end mediante 'senal_start'
        '''
        user = datos[0]
        length_check = parametros.MIN_CARACTERES <= len(user) <= parametros.MAX_CARACTERES
        alfanumerico = user.isalnum()
        not_void = len(user) != 0
        map_name = datos[1]
        data_set = [[length_check, alfanumerico, not_void], map_name + '.txt']
        self.senal_start.emit(data_set)
