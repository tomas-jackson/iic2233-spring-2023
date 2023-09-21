from collections import namedtuple
import parametros
from random import choice

# defino las namedtuples para representar mas facilmente cada excavador, arena, consumible o tesoro
# y ayudar con la lectura de codigo

Excavador = namedtuple('Excavador', ['name', 'type', 'age', 'energ', 'fuerza', 'luck', 'happy'])
Arenas = namedtuple('Arenas', ['name', 'type', 'rareza', 'humedad', 'dureza', 'estatica'])
Consumibles = namedtuple('Consumibles', ['name', 'descripcion', 'energ', 'fuerza', 'luck', 'happy'])
Tesoros = namedtuple('Tesoros', ['name', 'descripcion', 'calidad', 'cambio'])

# abajo de esta linea abro los archivos necesarios para extraer la informacion y dejo la info
# almacenada como namedtuples para cada objeto

with open(parametros.PATH_EXCAVADORES, 'r', encoding='UTF-8') as info_excavadores:
    lista_excavadores = [entry.strip().split(',') for entry in info_excavadores.readlines()[1:]]
    for i in range(len(lista_excavadores)):
        lista_excavadores[i] = Excavador(*lista_excavadores[i])

with open(parametros.PATH_ARENAS, 'r', encoding='UTF-8') as info_arenas:
    lista_arenas = [entry.strip().split(',') for entry in info_arenas.readlines()[1:]]
    for i in range(len(lista_arenas)):
        lista_arenas[i] = Arenas(*lista_arenas[i])

with open(parametros.PATH_CONSUMIBLES, 'r', encoding='UTF-8') as info_consumibles:
    lista_consumibles = [entry.strip().split(',') for entry in info_consumibles.readlines()[1:]]
    for i in range(len(lista_consumibles)):
        lista_consumibles[i] = Consumibles(*lista_consumibles[i])

with open(parametros.PATH_TESOROS, 'r', encoding='UTF-8') as info_tesoros:
    lista_tesoros = [entry.strip().split(',') for entry in info_tesoros.readlines()[1:]]
    for i in range(len(lista_tesoros)):
        lista_tesoros[i] = Tesoros(*lista_tesoros[i])

# cal

arenas_tipo_pedido = [entry for entry in lista_arenas if entry.type == parametros.ARENA_INICIAL]
eleccion = choice(arenas_tipo_pedido)
lista_arenas.remove(eleccion)
arena_inicial = eleccion
